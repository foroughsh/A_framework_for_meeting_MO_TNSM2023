import pandas as pd
import sys
import argparse
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == "__main__":
    args = sys.argv
    parser = argparse.ArgumentParser(description='Please check the code for options!')
    parser.add_argument("--path_to_artifacts", type=str, default="../../../artifacts/")
    parser.add_argument("--data_file_name", type=str, default="data.csv")


    args = parser.parse_args()

    path_to_artifacts = args.path_to_artifacts
    file_name = args.data_file_name

    data = pd.read_csv(path_to_artifacts + file_name)
    data = data[data["max_l1"]<4]
    data = data[data["d1"] < 1]

    fig_width = 7
    fig_hight = 3.6
    font_size = 16
    transparency = 0.2

    fig, ax1 = plt.subplots(1, 1, sharex=True, figsize=(fig_width, fig_hight))

    ax1.plot(data["d1"], c="b", label="response time")

    ax1.set_ylabel("Response \n time (sec)", fontsize=font_size)
    ax1.set_xlabel("Time index", fontsize=font_size)

    ax1.tick_params(axis='both', which='major', labelsize=font_size)
    ax1.tick_params(axis='both', which='minor', labelsize=font_size)

    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    plt.grid(False)

    plt.rcParams['savefig.dpi'] = 200
    plt.tight_layout()
    plt.show()

    fig_width = 10
    fig_hight = 10

    fig, ax1 = plt.subplots(1, 1, sharex=True, figsize=(fig_width, fig_hight))

    corr = data[data.columns].corr()
    sns.heatmap(corr, vmin=corr.values.min(),
                vmax=1,
                square=True,
                cmap="YlGnBu",
                linewidths=0.1,
                annot=True,
                annot_kws={"fontsize": 14}, fmt=".2f", ax=ax1)
    plt.tight_layout()
    plt.savefig("data_after_heatmap.pdf")
    plt.show()

    print("The average response time is: ", data["d1"].mean())