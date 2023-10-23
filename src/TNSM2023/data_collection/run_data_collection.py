import sys
import argparse
import time

import math
from TNSM2023.data_collection.data_collection import DataCollection

if __name__ == "__main__":
    args = sys.argv

    if (len(args) > 1):
        parser = argparse.ArgumentParser(description='Please check the code for options!')
        parser.add_argument("--IP_port", type=str, default="172.31.212.81:30048")
        parser.add_argument("--path_to_data_file", type=str, default="data.csv")
        parser.add_argument("--path_to_artifacts", type=str, default="../artifacts/")
        parser.add_argument("--path_to_LG", type=str, default="./")
        parser.add_argument("--path_to_config_files", type=str, default="../cluster_configuration_files/")


        args = parser.parse_args()

        IP_port = args.IP_port
        path_to_data_file = args.path_to_data_file
        path_to_artifacts = args.path_to_artifacts
        path_to_LG = args.path_to_LG
        path_to_config_files = args.path_to_config_files


        service = dict()
        service["name"] = "compute"
        service["l"] = 1
        service["p"]=20
        service["b"]=int(math.ceil((1-0.2) * service["l"]))
        service["c"]=1
        services = [service]

        data_collection = DataCollection(IP_port=IP_port, data_file_name=path_to_data_file,
                                         path_to_artifacts=path_to_artifacts, path_to_LG=path_to_LG,
                                         path_to_config_files=path_to_config_files, services=services)

        load = [4,8,12]
        cpu = range(1,6)
        routing_blocking = [0, 0.2, 0.4, 0.6, 0.8, 1]
        data_collection.kill_load_generator()
        time.sleep(5)
        for l in load:
            service["l"] = l
            data_collection.run_load_generator(service["name"],l)
            for c in cpu:
                service["c"] = c
                for p in routing_blocking:
                    service["p"] = p * 100
                    for b in routing_blocking:
                        service["b"] = (1-b) * service["l"]
                        data_collection.set_services(services=[service])
                        data_collection.data_collection()
            data_collection.kill_load_generator()

    else:
        print(
            "Please enter the file name for your learning curve! The list of options are as the following:\n"
            "\t--IP_port x.x.x.x:yyyy\n"
            "\t--path_to_data_file path_to_data_file\n"
            "\t--path_to_artifacts path_to_artifacts\n"
            "\t--path_to_LG path_to_LG"
            "\t--path_to_config_files path_to_config_files"
        )
