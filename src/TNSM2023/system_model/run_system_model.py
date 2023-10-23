import sys
import argparse
import logging
from TNSM2023.system_model.learning_system_model import SystemModel


# number_of_estimators:int, data_file_name:str, artifacts:str
if __name__ == "__main__":
    args = sys.argv

    parser = argparse.ArgumentParser(description='Please check the code for options!')
    parser.add_argument("--number_of_estimators", type=int, default=120)
    parser.add_argument("--data_file_name", type=str, default="data.csv")
    parser.add_argument("--artifacts", type=str, default="../../../artifacts/")
    parser.add_argument("--target_file_name", type=str, default="system_model")


    args = parser.parse_args()

    number_of_estimators = args.number_of_estimators
    data_file_name = args.data_file_name
    artifacts = args.artifacts
    target_file_name = args.target_file_name

    system_model = SystemModel(number_of_estimators=number_of_estimators, data_file_name=data_file_name,
                               artifacts=artifacts)

    x_features = ["max_l1", "l1", "cl1", "p1", "b1", "c1"]
    y_features = ["d1"]

    print(system_model.data_file_name)
    test_nmae, train_nmae, test_r2score, train_r2score, avg_error = system_model.learn_system_model(x_features=x_features,
                                                                                         y_features=y_features)
    system_model.save_model("system_model")
    # logging.info("==== System model test NMAE is " + str(test_nmae))
    # logging.info("==== System model train NMAE is " + str(train_nmae))
    # logging.info("==== System model test R2 is " + str(test_r2score))
    # logging.info("==== System model train R2 is " + str(train_r2score))

    print("==== System model test NMAE is " + str(test_nmae))
    print("==== System model train NMAE is " + str(train_nmae))
    print("==== System model test R2 is " + str(test_r2score))
    print("==== System model train R2 is " + str(train_r2score))
    print("==== System model average error is " + str(avg_error))
