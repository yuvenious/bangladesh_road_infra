import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import sin, cos, atan2, sqrt, pi, radians
import statsmodels.api as sm
from clean_module import smoothing

def randomize(df_road, road_num = 0, frac = 10, s = 0.01, dis = 1, show_iter = False):
    df_original = pd.DataFrame(df_road['data_frame'].iloc[road_num])[["lon", "lat"]]
    """
    1. before clean
    2. after 1st clean
    3. randomize
    4. after 2nd clean
    """
    df1 = df_original[["lon", "lat"]]
    df2 = smoothing(df1[["lon", "lat"]])
    df3 = df_original[["lon", "lat"]]
    df4 = df_original[["lon", "lat"]]

    plt.figure(figsize = (15,7))
    f = frac/100
    df_rand = df3[["lat", "lon"]].sample(frac = f)
    ran_mul1 = np.random.randn(len(df_rand))
    ran_mul2 = np.random.randn(len(df_rand))
    df_rand["lat"] = df_rand["lat"] + ran_mul1 * s
    df_rand["lon"] = df_rand["lon"] + ran_mul2 * s
    df3.loc[df_rand.index, ["lat", "lon"]] = df_rand[["lat", "lon"]]
    df4 = smoothing(df3[["lat", "lon"]], dis = dis, show_iter = show_iter)

    # Randomization
    plt.subplot(1,2,1)
    plt.plot(df2["lat"], df2["lon"], lw = 5, color = "blue", alpha = 0.2,
             label = "Road data")
    plt.plot(df3["lat"], df3["lon"], color = "red",
             label = "Randomized data")
#     plt.scatter(df3["lat"][df_rand.index], df3["lon"][df_rand.index], color = "red", marker = "+", s = 100,
#                 label = "Random Noise Addition")
    plt.xlim(min(df2["lat"]), max(df2["lat"]))
    plt.ylim(min(df2["lon"]), max(df2["lon"]))
    plt.legend()
    plt.title("Randomization")

    #Cleaning
    plt.subplot(1,2,2)
    plt.plot(df2["lat"], df2["lon"], lw = 5, color = "blue", alpha = 0.2,
             label = "Road data")
    # plt.scatter(df3["lat"][df_rand.index], df3["lon"][df_rand.index], color = "red", marker = "+", s = 100,
    #             label = "Random Noise Addition")
    plt.plot(df4["lat"], df4["lon"], color = "green",
             label = "Second Cleaning")
#     plt.scatter(df4["lat"][df_rand.index], df4["lon"][df_rand.index],
#                 s = 200, facecolors = "none", edgecolors = "red", linewidths = 1,
#                 label = "Fixed after Randomization")
    plt.xlim(min(df2["lat"]), max(df2["lat"]))
    plt.ylim(min(df2["lon"]), max(df2["lon"]))
    plt.legend()
    plt.title("After Cleaning")
