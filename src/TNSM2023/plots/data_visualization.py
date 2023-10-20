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
    # plt.rc('text', usetex=True)
    # # plt.rc('text.latex', preamble=r'\usepackage{amsfonts,amsmath}')
    # plt.rcParams['axes.linewidth'] = 0.8
    # plt.rcParams.update({'font.size': font_size})
    # plt.rcParams['font.family'] = ['serif']

    fig, ax1 = plt.subplots(1, 1, sharex=True, figsize=(fig_width, fig_hight))

    ax1.plot(data["d1"], c="b", label="response time")

    # ax1.axvline(x=19, color='k', label='Change point', linestyle="--")
    # ax1.axhline(y=0.10, color='y', alpha=1.0, linestyle="--", label="$O_1$")

    ax1.set_ylabel("Response \n time (sec)", fontsize=font_size)
    ax1.set_xlabel("Time index", fontsize=font_size)

    # # Shrink current axis's height by 10% on the bottom
    # box = ax1.get_position()
    #
    # # Put a legend below current axis
    # ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.4),
    #            fancybox=True, shadow=False, ncol=2, fontsize=font_size - 4)

    ax1.tick_params(axis='both', which='major', labelsize=font_size)
    ax1.tick_params(axis='both', which='minor', labelsize=font_size)

    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    plt.grid(False)

    plt.rcParams['savefig.dpi'] = 200
    plt.tight_layout()
    # plt.savefig("sc3_eval_on_sim_response.pdf", bbox_inches='tight')
    # visualizing plot using matplotlib.pyplot library
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
    # print(corr)

    print("The average response time is: ", data["d1"].mean())