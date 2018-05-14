import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import sin, cos, atan2, sqrt, pi, radians
import statsmodels.api as sm

# This function defines the distance between two locations.
def distance(loc1, loc2, R = 6380):
    #change the value into radians
    lat1 = radians(float(loc1[0]))
    lon1 = radians(float(loc1[1]))

    lat2 = radians(float(loc2[0]))
    lon2 = radians(float(loc2[1]))

    #calculate the distance
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
    c = 2 * atan2( sqrt(a), sqrt(1-a) )
    d = R * c # where R is the radius of the Earth
    return d

def visual_check(df, n = 5, cols = ['lat', 'lon'], nbr = 20, bar = 0.001, dis = 10, names = ["Latitude", "Longitude"]):
    """
    Main Purpose: "Detection" of abnormal points
    1. Outliers(i.e. out-of-trend) by fitting into the (estimated) true trend (defined by local regression)
    2. Far-away points which have further distance than 10km (10km can be adjusted by the parameter 'dis')
    """
    x = np.linspace(0,1,len(df))
    frac = nbr/len(df)
    df['x'] = x

#     distance checker between two neiboring points
    d = []
    for i in range(len(df)-1):
        loc1 = [df[cols].iloc[i][0], df[cols].iloc[i][1]]
        loc2 = [df[cols].iloc[i+1][0], df[cols].iloc[i+1][1]]
        d.append(distance(loc1, loc2))
    df['distance'] = np.array([None] + d)


#     plot
    plt.figure(figsize = (15, 7))
    for i in range(len(cols)):
        y = df[cols[i]]
#         lowess will returns a smoothed data set, namely the "true trend line"
        lowess = sm.nonparametric.lowess(y, x, frac)
        yest = list(zip(*lowess))[1]

        df['est'] = yest
        df['ratio'] = abs(y/yest - 1)
        suspicious = df.sort_values(by = 'ratio', ascending = False)[:n]

        plt.subplot(1, len(cols), i+1)

#         plot data
        plt.plot(x, y, label='Road data', ls = '--')

#         plot trend line
        plt.plot(x, yest, label='True location (estimated trend)', lw = 5, alpha = 0.2, color = 'red')

#         plot far-away points
        plt.scatter(x[np.array(df['distance'] > dis)], y[df['distance'] > dis],color = 'green',
                    label = 'far away >{dis} km'.format(dis = dis))

#         plot outliers
        plt.scatter(x[np.array(abs(y/yest - 1) > bar)], y[abs(y/yest - 1) > bar], s = 50, color = 'black',
                    label='outliers (>{bar}% deviation)'.format(bar = bar * 100))

#         plot top 5 suspicious points
        plt.scatter(suspicious['x'], suspicious[cols[i]],
                    marker = "o", s = 100, facecolors = "none", edgecolors = 'red', linewidths = 2,
                    label='top {num}'.format(num = n))
        plt.ylabel(names[i], size = 14)
        plt.title("{name} Decomposition".format(name = names[i]), size = 20)
        plt.legend(fontsize = "large")

#         print(suspicious[["road", "chainage", "lrp", "lat", "lon"]])
#         print("num outliers: ", sum(abs(y/yest - 1) > bar))

def smoothing(df, cols = ['lat', 'lon'], nbr = 20, bar = 0.001, dis = 10, show_iter = True):
    """
    Correcting algorithm
    1. Outliers: Fit to the trend line
    2. Far-away points: Drop and Interpolate
    3. Iterate 1 and 2, until no such points are observed.
    """
#     iterate running the script until no outliers and far-away points are detected.
    num_strange = [1, 1, 1]
    count = 0
    while (sum(num_strange) > 0):
        count += 1
        if show_iter:
            print(count, "iteration(s)")
#         1. outliers correction
        x = np.linspace(0,1,len(df))
        frac = nbr/len(df)
        df['x'] = x

        num_strange = [1,1,1]

        for i in range(len(cols)):
#             run local regression
            y = df[cols[i]]
            lowess = sm.nonparametric.lowess(y, x, frac)
            yest = np.array(list(zip(*lowess))[1])

#             record the number of outliers
            num_strange[i] = sum(abs(y/yest - 1) > bar)

#             fit outliers to the estimated trend
            idx = y[abs(y/yest - 1) > bar].index
            new_val = yest[np.array(abs(y/yest - 1) > bar)]
            y = y.where(abs(y/yest - 1) <= bar)
            d = dict(zip(idx, new_val))
            y.fillna(d, inplace = True)
            df[cols[i]] = y

#         2. far-away points correction
        d = []
        for i in range(len(df)-1):
            loc1 = [df[cols].iloc[i][0], df[cols].iloc[i][1]]
            loc2 = [df[cols].iloc[i+1][0], df[cols].iloc[i+1][1]]
            d.append(distance(loc1, loc2))
        df['distance'] = np.array([None] + d)

#         record the number of far-away points
        num_strange[2] = len(df.where(df['distance'] > dis).dropna())

#         interpolate far-away points
        df.loc[df.where(df['distance'] > dis).dropna().index, ["lat", "lon"]] = None
        df[['lat', 'lon']] = df[['lat', 'lon']].interpolate()

    return df
