import sys
import argparse

if __name__ == "__main__":
    args = sys.argv
    parser = argparse.ArgumentParser(description='Please check the code for options!')
    parser.add_argument("--path_to_artifacts", type=str, default="../../../artifacts/")
    parser.add_argument("--data_file_name", type=str, default="data_k8_sc1.csv")
    parser.add_argument("--path_to_LG", type=str, default="../data_collection/")

    args = parser.parse_args()

    path_to_artifacts = args.path_to_artifacts
    file_name = args.data_file_name
    path_to_LG = args.path_to_LG



