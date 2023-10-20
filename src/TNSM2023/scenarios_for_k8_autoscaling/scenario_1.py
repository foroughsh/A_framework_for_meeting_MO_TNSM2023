import sys
import argparse
import time
from typing import List
from TNSM2023.data_collection.data_collection import DataCollection

def read_load_from_file(file_name:str) -> List[int]:
    load = []
    with open(file_name, "r") as file:
        lines = file.readlines()

    for line in lines:
        load.append(int(line))

    return load

if __name__ == "__main__":
    args = sys.argv
    parser = argparse.ArgumentParser(description='Please check the code for options!')
    parser.add_argument("--path_to_artifacts", type=str, default="../../../artifacts/")
    parser.add_argument("--data_file_name", type=str, default="data_k8_sc1.csv")
    parser.add_argument("--path_to_LG", type=str, default="../data_collection/")
    parser.add_argument("--load_file_name", type=str, default="random_load.csv")
    parser.add_argument("--IP_port", type=str, default="172.31.212.81:30048")
    parser.add_argument("--path_to_config_file", type=str, default="../../../cluster_configuration_files/")

    args = parser.parse_args()

    path_to_artifacts = args.path_to_artifacts
    file_name = args.data_file_name
    path_to_LG = args.path_to_LG
    path_to_load = args.load_file_name
    IP_port = args.IP_port
    data_file_name = args.data_file_name
    path_to_config_file = args.path_to_config_file

    service = dict()
    service["name"] = "compute"
    service["l"] = 1
    service["p"] = 80
    service["b"] = service["l"]
    service["c"] = 1
    services = [service]

    data_collection = DataCollection(IP_port=IP_port, data_file_name=data_file_name, path_to_artifacts=path_to_artifacts,
                                     path_to_LG=path_to_LG, path_to_config_files=path_to_config_file, services=services,
                                     n=10)

    load = read_load_from_file(path_to_artifacts + path_to_load)

    data_collection.apply_service_config()
    time.sleep(data_collection.settling_time)

    for l in load:
        service["l"] = l
        data_collection.set_services(services=[service])
        data_collection.run_load_generator(service["name"], l)
        time.sleep(data_collection.time_step)
        data_collection.collect_samples_k8()
        data_collection.kill_load_generator()






