import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import binned_statistic_2d


def read_csvs(path):
    left_zas = pd.read_csv("/tmp/camera_right.csv")
    right_zas = pd.read_csv("/tmp/camera_left.csv")
    return left_zas, right_zas


def both_one_vs_other(left, right):
    left_max_value = np.max(np.abs(np.hstack((left["err_x"], left["err_y"]))))
    right_max_value = np.max(np.abs(np.hstack((right["err_x"], right["err_y"]))))
    max_value = left_max_value if left_max_value > right_max_value else right_max_value
    fig, (ax1, ax2) = plt.subplots(1,2)

    sns.scatterplot(x=left["err_x"], y=left["err_y"], ax=ax1, color="r")
    sns.scatterplot(x=right["err_x"], y=right["err_y"], ax=ax2, color="b")

    ax1.set_title("Left camera")
    ax1.set_xlim(-max_value*1.2, max_value*1.2)
    ax1.set_ylim(-max_value*1.2, max_value*1.2)

    ax2.set_title("Right camera")
    ax2.set_xlim(-max_value*1.2, max_value*1.2)
    ax2.set_ylim(-max_value*1.2, max_value*1.2)

    plt.show()


def both_rms_center(left, right, img_width_, img_height_):
    left_normalized_x = left["obs_x"] - (img_width_/2)
    left_normalized_y = left["obs_y"] - (img_height_/2)
    
    right_normalized_x = right["obs_x"] - (img_width_/2)
    right_normalized_y = right["obs_y"] - (img_height_/2)

    left_distance_to_center = np.sqrt((left_normalized_x * left_normalized_x) + (left_normalized_y * left_normalized_y))
    right_distance_to_center = np.sqrt((right_normalized_x * right_normalized_x) + (right_normalized_y * right_normalized_y))

    left_rms_err = np.linalg.norm([left["err_x"], left["err_y"]], axis=0)
    right_rms_err = np.linalg.norm([right["err_x"], right["err_y"]], axis=0)

    left_corr = np.corrcoef(left_distance_to_center, left_rms_err)
    right_corr = np.corrcoef(right_distance_to_center, right_rms_err)

    fig, (ax1, ax2) = plt.subplots(1, 2)
    #print("CORRELATION ", corr[0][1])
    sns.scatterplot(x=left_distance_to_center, y=left_rms_err, ax=ax1, color="r")
    sns.scatterplot(x=right_distance_to_center, y=left_rms_err, ax=ax2, color="b")
    #corr_str = "Correlation " + str(corr[0][1])
    ax1.set_title("Left camera RMS vs distance to center")
    ax2.set_title("Right camera RMS")
    #plt.text(0.7 * np.max(distance_to_center), 0.9 * np.max(rms_err), corr_str)
    plt.show()


def stereo_reproj_location(left, right, img_width_, img_height_, bin_size_):
    width_bins = list(range(0, img_width_, bin_size_))
    height_bins = list(range(0, img_height_, bin_size_))

    err_df_left = [left["err_x"], left["err_y"]]
    err_df_right = [right["err_x"], right["err_y"]]

    err_rms_left = np.sqrt(np.square(err_df_left).sum(axis=0))
    err_rms_right = np.sqrt(np.square(err_df_right).sum(axis=0))

    fig, (ax1, ax2) = plt.subplots(1,2)
    bins_left = binned_statistic_2d(left["obs_x"], left["obs_y"], err_rms_left, statistic='mean', bins=[width_bins, height_bins])
    err_img_bins_left = np.nan_to_num(bins_left.statistic, nan=0.0)
    sns.heatmap(err_img_bins_left, ax=ax1)

    bins_right = binned_statistic_2d(right["obs_x"], right["obs_y"], err_rms_right, statistic='mean', bins=[width_bins, height_bins])
    err_img_bins_right = np.nan_to_num(bins_right.statistic, nan=0.0)
    sns.heatmap(err_img_bins_right, ax=ax2)

    plt.show()



bin_size = 30
img_width = 1544
img_height = 2040

zas = pd.read_csv("/tmp/camera_right.csv")
err_df = [zas["err_x"], zas["err_y"]]

err_rms = np.sqrt(np.square(err_df).sum(axis=0))
print(err_rms)
sb_data = [zas["obs_x"], zas["obs_y"], err_rms]

# X vs Y scatter
left_pd, right_pd = read_csvs("aaa")

# Reprojection error vs image location
stereo_reproj_location(left_pd, right_pd, img_width, img_height, 10)
both_one_vs_other(left_pd, right_pd)

# RMS vs distance to center
both_rms_center(left_pd, right_pd, img_width, img_height)

# Error over images
img_nums = zas["pattern_num"]
rms_err = np.linalg.norm([zas["err_x"], zas["err_y"]], axis=0)

plt.figure()
sns.scatterplot(x=img_nums, y=rms_err)
#corr_str = "Correlation " + str(corr[0][1])
plt.title("img number vs rms")
plt.show()

# XY error vs angle difference to vertical
rms_err = np.linalg.norm([zas["err_x"], zas["err_y"]], axis=0)
err = np.abs(zas["err_y"]) #rms_err

vertical = [zas["r"][0], zas["p"][0], zas["yaw"][0]]
diff_r = (zas["r"] - zas["r"][0])
diff_p = (zas["p"] - zas["p"][0])
diff_yaw = (zas["yaw"] - zas["yaw"][0])

plt.figure()
sns.scatterplot(x=diff_r, y=err)
plt.title("r diff to vertical")
plt.show()

plt.figure()
sns.scatterplot(x=diff_p, y=err)
plt.title("p diff to vertical")
plt.show()

plt.figure()
sns.scatterplot(x=diff_yaw, y=err)
plt.title("yaw diff to vertical")
plt.show()



