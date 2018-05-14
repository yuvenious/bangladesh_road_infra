"""
LIVE BAR PLOT
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

interval = 1000
segs = ["seg1", "seg2", "seg3", "seg4"]

def animate(i):
    df = update_df(normalize = True)

    segs_title = ["Segment1", "Segment2", "Segment3", "Segment4"]
    width = 0.35
    ymax = 2.0
    fontsize = 13
    titlesize = 15
    for i in range(len(segs)):
        ax = plt.subplot(1,len(segs),i+1)
        x = np.arange(len(df.columns.levels[2]))
        stats = ["num", "time"]
        labels = ["Criticality", "Vulnerability"]
        ys = []
        ax.clear()
        for j in range(len(stats)):
            y = df.loc[:,(segs[i], stats[j], slice(None))].mean()
            ys.append(y)
            bottom = 0
            if j != 0:
                bottom = ys[0].values
            ax.bar(x, y, width, bottom = bottom, label = labels[j])
        plt.xticks(x, df.columns.levels[2], fontsize = fontsize)
        plt.ylim(0,ymax)
        plt.yticks(np.linspace(0,ymax, num = 5), fontsize = fontsize)
        plt.grid()
        plt.tight_layout()
        plt.title("%s"%segs_title[i], fontsize = titlesize)
        plt.legend(fontsize = 13)
fig = plt.figure(figsize = (15,6))
df = update_df(normalize = True)
ani = animation.FuncAnimation(fig, animate, interval=interval)
plt.show()
