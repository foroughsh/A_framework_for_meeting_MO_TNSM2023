import sys
import argparse
from TNSM2023.system_model.learning_system_model import SystemModel


# number_of_estimators:int, data_file_name:str, artifacts:str
if __name__ == "__main__":
    args = sys.argv

    if (len(args) > 1):
        parser = argparse.ArgumentParser(description='Please check the code for options!')
        parser.add_argument("--number_of_estimators", type=int, default=120)
        parser.add_argument("--data_file_name", type=str, default="data.csv")
        parser.add_argument("--artifacts", type=str, default="../artifacts/")
        parser.add_argument("--target_file_name", type=str, default="system_model")


        args = parser.parse_args()

        number_of_estimators = args.number_of_estimators
        data_file_name = args.data_file_name
        artifacts = args.artifacts
        target_file_name = args.target_file_name

        system_model = SystemModel()
        system_model.learn_system_model(x_features=[], y_features=[], )