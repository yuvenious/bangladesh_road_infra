import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import sin, cos, atan2, sqrt, pi, radians
import statsmodels.api as sm

def bagging(df_road, road_id, axis, f_sam = .7, n_sam = 100):
    # select either longitude or latitude
    i = axis
    # parameters for sampling
    #parameters for data training
    nbr = 20
    bar = 0.1
    df = pd.DataFrame(df_road['data_frame'].iloc[road_id])[["lon", "lat"]]
    # print("number of data points:", len(df))
    cols  = ["lon", "lat"]
    
    plt.figure(figsize = (15, 7))
    """
    1. General training
    """
    # plot the data
    plt.subplot(1,2,1)
    x_ori = np.linspace(0, 1, len(df))
    y_ori = df[cols[i]]
    plt.plot(x_ori, y_ori, label = "Data")

    # training the entire data
    f_nbr = nbr / len(df)
    lowess = sm.nonparametric.lowess(y_ori, x_ori, frac = f_nbr)
    yest_ori = list(zip(*lowess))[1]

    #plot the trend
    plt.plot(x_ori, yest_ori, lw = 5, alpha = 0.5, label = "Estimated true location")

    # abnormal point detection
    rng = max(y_ori) - min(y_ori)
    out = np.where(abs(yest_ori - y_ori)/rng > bar)
    plt.scatter(x_ori[out], y_ori.iloc[out], marker = "x", color = "red", label = "outlier")
    plt.title("General training", size = 15)
    plt.ylabel("Longitude", size = 13)
    plt.legend(fontsize = "x-large")

    """
    2. Training with bagging method
    """
    # sample data
    df_rand = df[["lat", "lon"]].sample(frac = f_sam).sort_index()

    # plot the sample
    plt.subplot(1,2,2)
    x_ran = np.linspace(0, 1, len(df_rand))
    y_ran = df_rand[cols[i]]
    plt.plot(x_ori, y_ori, label = "Data")

    # training the data by ensemble machine learning
    from scipy.interpolate import interp1d

    sam_yests = []
    ori_yests = []
    for j in range(n_sam):
        df_rand = df[["lat", "lon"]].sample(frac = f_sam).sort_index()
        x = np.linspace(0,1,len(df_rand))
        y = df_rand[cols[i]]
        f = nbr / len(df_rand)
        lowess = sm.nonparametric.lowess(y, x, frac = f)
        lowess_x = list(zip(*lowess))[0]
        lowess_y = list(zip(*lowess))[1]
        f = interp1d(lowess_x, lowess_y, bounds_error=False)
        sam_yests.append(lowess_y)
        ori_yests.append(f(x_ori))
    sam_yest = np.array(sam_yests).mean(axis = 0)
    ori_yest = np.array(ori_yests).mean(axis = 0)

    plt.plot(x_ori, ori_yest, lw = 5, alpha = 0.5, label = "Estimated true location")

    # abnormal point detection
    rng = max(y_ori) - min(y_ori)
    out = np.where(abs(ori_yest - y_ori)/rng > bar)
    plt.scatter(x_ori[out], y_ori.iloc[out], marker = "x", color = "red", label = "outlier")
    plt.ylabel("Longitude", size = 13)
    # print("number of outliers:", len(out[0]))
    plt.title("Training by bagging", size = 15)
    plt.legend(fontsize = "x-large")
