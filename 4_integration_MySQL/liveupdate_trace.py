"""
LIVE TRACE PLOT
"""
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import pandas as pd
import numpy as np

db = create_engine("mysql://epa1351group1:epa1351@localhost/world")
query = ("SELECT * FROM simio")

def norm(df):
    df = df.dropna()
    df = df / df.max().max()
    return df

def update_df(normalize = False):
    # create pandas dataframe and reset wrong simulation index
    df = pd.read_sql_query(query, db, index_col='Id').reset_index(drop=True)
    # rename column headers
    cols = []
    cols.append("Q")
    cols = cols + list(
        np.tile(["seg1", "seg2", "seg3", "seg4"], 6).astype(object)
        + np.repeat("_", 24).astype(object)
        + np.repeat(["time", "num"], 12).astype(object)
        + np.repeat("_", 24).astype(object)
        + np.tile(np.repeat(["bus", "truck", "other"], 4), 2).astype(object))
    cols.append("DateTime")
    df.columns = cols

    time_col = cols[1:13]
    num_col = cols[13:25]
    df_time = df[time_col]
    df_num = df[num_col]

    df = df[time_col + num_col]
    df = df.dropna()
    df.sort_index(axis=1, inplace=True)
    df.columns = df.columns.str.split('_', expand = True)

    if normalize:
        # normalizing data for vulnerabiltiy and criticality
        # 1. Travel Time -> Delay Time
        expected_time = pd.read_csv("expected_time.csv")
        expected_time.drop(["Network", "LogicalLength"], axis = 1, inplace = True)
        expected_time.index = ["seg1", "seg2", "seg3", "seg4"]
        expected_time = expected_time[["bus", "other", "truck"]]
        df.loc[:, (slice(None), "time")] = df.loc[:, (slice(None), "time")].apply(lambda x: x/5/expected_time.stack().values, axis = 1)

        # 2. Number of Entity
        df.loc[:, (slice(None), "num")] = norm(df.loc[:, (slice(None), "num")])

    return df

df = update_df()
simtimemax = 500
interval = 1000 # mil-second
entitymax = df.loc[:, (slice(None), "num")].max().max()+10
timemax = df.loc[:, (slice(None), "time")].max().max()+5

# Specify which segments/statistics/transporters to show
segs = ["seg1", "seg2", "seg3", "seg4"]
stats = ["time", "num"]
stats_string = ["time in segment (hr)", "# in segment"]
trans = ["bus", "truck", "other"]

# Number of Plots shall be drawn
num_plot = len(segs)*len(stats)*len(trans)

# Subplots' properties
if num_plot >= 12:
    ncols = 6
else:
    ncols = max(len(segs),len(stats),len(trans))
nrows = int(num_plot/ncols)
if num_plot > 2:
    locs = list(zip(np.repeat(np.arange(nrows), ncols), np.tile(np.arange(ncols), nrows)))
else:
    locs = [0,1]
# Create objects
fig, axes = plt.subplots(ncols=ncols, nrows=nrows, figsize = (ncols * 3, nrows * 3), sharex = True)

def animate(i):
    df = update_df()
    count = 0
    for i in range(len(segs)):
        for j in range(len(stats)):
            for k in range(len(trans)):
                df_plot = df.loc[:, (segs[i], stats[j], trans[k])]
                axes[locs[count]].clear()
                axes[locs[count]].plot(df_plot)
                axes[locs[count]].set_xlabel("simulation time (hr)")
                axes[locs[count]].set_xlim(0,simtimemax)
                axes[locs[count]].set_ylabel("%s" %stats_string[j])
                if j == 0:
                    axes[locs[count]].set_ylim(0, timemax)
                else:
                    axes[locs[count]].set_ylim(0, entitymax)
                axes[locs[count]].set_title("%s in %s" %(trans[k], segs[i]))
                count = count + 1
    fig.tight_layout()
# Update every interval
ani = animation.FuncAnimation(fig, animate, interval=interval)
plt.show()
