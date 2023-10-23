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

    # data = pd.read_csv(path_to_artifacts + file_name)
    data_noop = pd.read_csv(path_to_artifacts + "data_noop.csv")
    data_k8 = pd.read_csv(path_to_artifacts + "data_k8_sc1_80_no_routing.csv")
    # data = data[data["max_l1"]<4]
    # data = data[data["d1"] < 1]

    fig_width = 7
    fig_hight = 3.6
    font_size = 12
    transparency = 0.8

    fig, ax1 = plt.subplots(2, 1, sharex=True, figsize=(fig_width, fig_hight))

    ax1[1].plot(data_noop["d1"], c="royalblue", alpha = transparency, label="Without applying any policy")
    ax1[1].plot(data_k8["d1"], c="crimson", alpha = transparency, label="K8 autoscaling")

    ax1[1].axhline(y=1.0, color='y', alpha=1.0, linestyle="--", label="$O_1$")

    ax1[1].set_ylabel("Response \n time (sec)", fontsize=font_size)
    ax1[1].set_xlabel("Time index", fontsize=font_size)

    ax1[1].tick_params(axis='both', which='major', labelsize=font_size)
    ax1[1].tick_params(axis='both', which='minor', labelsize=font_size)

    # Shrink current axis's height by 10% on the bottom
    box = ax1[1].get_position()

    # Put a legend below current axis
    ax1[1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.4),
               fancybox=True, shadow=False, ncol=2, fontsize=font_size - 4)

    plt.yscale("log")

    ax1[1].spines['top'].set_visible(False)
    ax1[1].spines['right'].set_visible(False)
    plt.grid(False)

    ax1[0].plot(data_k8["l1"], c="rebeccapurple")

    ax1[0].set_ylabel("Load (req/sec)", fontsize=font_size)

    ax1[0].tick_params(axis='both', which='major', labelsize=font_size)
    ax1[0].tick_params(axis='both', which='minor', labelsize=font_size)
    ax1[0].spines['top'].set_visible(False)
    ax1[0].spines['right'].set_visible(False)

    # ax2 = ax1.twinx()
    # ax2.plot(data_noop["l1"], c="violet", alpha = transparency, label="Offered load")

    plt.rcParams['savefig.dpi'] = 200
    plt.tight_layout()
    plt.show()

    fig_width = 10
    fig_hight = 10

    fig, ax1 = plt.subplots(1, 1, sharex=True, figsize=(fig_width, fig_hight))

    corr = data_k8[data_k8.columns].corr()
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

    print("The average response time is: ", data_k8["d1"].mean())