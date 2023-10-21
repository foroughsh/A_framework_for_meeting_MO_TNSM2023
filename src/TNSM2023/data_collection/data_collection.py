import numpy as np
import subprocess
import time
import os
from pathlib import Path
from typing import List, Dict
import logging
from TNSM2023.data_collection.run_commands_on_cluster import RunCommandsOnCluster

class DataCollection:
    def __init__(self, IP_port:str, data_file_name:str, path_to_artifacts:str, path_to_LG:str, path_to_config_files:str,
                 services:List[Dict], time_step:int = 5, settling_time = 5, n:int = 5) -> None:
        self.IP_port = IP_port
        self.artifacts = path_to_artifacts
        self.path_to_config_files = path_to_config_files
        self.time_step = time_step
        self.settling_time = settling_time
        self.data_file_name = data_file_name
        self.path_to_LG = path_to_LG
        self.services = services
        self.n = n
        line = ""
        for i in range(1,len(self.services)+1):
            line = ("max_l" + str(i) + ",l" + str(i) + ",cl" + str(i) + ",p" + str(i) + ",b" + str(i) + ",c" + str(i) + ",d" + str(i) +
                    ",d" + str(i) + "_std,d" + str(i) + "1,d" + str(i) + "1_std,d" + str(i) + "2,d" + str(i) +
                    "2_std,drop" + str(i) + "\n")
        with open(self.artifacts + self.data_file_name, "w") as file:
            file.write(line)
        file.close()

    def run_load_generator(self, LG_name:str, load_value:float) -> None:
        '''
        This function starts the asyn load genrator with the constant load pattern and the given load value
        :param LG_name:
        :param load_value:
        :return:
        '''
        # Define the shell command to run
        shell_cmd = "nohup python " + self.path_to_LG + "async_load_generator.py " + LG_name + " constant " + str(
            load_value) + " " + self.IP_port + " " + self.artifacts + " > /dev/null &"

        # Run the command in the background
        subprocess.Popen(shell_cmd, shell=True)

    def kill_load_generator(self) -> None:
        # Define the shell command to run
        shell_cmd = "pkill -f async_load_generator.py"

        # Run the command in the background
        subprocess.Popen(shell_cmd, shell=True)

    def get_load_pattern(self, file_name:str) -> List[float]:
        with open(file_name) as file:
            lines = file.readlines()
        file.close()
        load_pattern = []
        for line in lines:
            load_pattern.append(float(line))
        return load_pattern

    def cleanup_files(self, services: List[Dict]) -> None:
        for service in services:
            path = Path(self.artifacts + "load_" + service["name"] + ".txt")
            if (path.is_file()):
                os.remove(self.artifacts  + "load_" + service["name"] + ".txt")
            path = Path(self.artifacts  + "response_" + service["name"] + ".txt")
            if (path.is_file()):
                os.remove(self.artifacts  + "response_" + service["name"] + ".txt")

    def clean_file_contents(self, services: List[Dict]) -> None:
        for service in services:
            with open(self.artifacts + "load_" + service["name"] + ".txt","w") as file:
                file.write("")
            file.close()
            with open(self.artifacts + "response_" + service["name"] + ".txt","w") as file:
                file.write("")
            file.close()

    def read_loads(self, services: List[Dict]) -> List[int]:
        offeted_loads = []
        for service_names in services:
            with open(self.artifacts + "load_" + service_names["name"] + ".txt","r") as file:
                lines = file.readlines()
            file.close()
            offeted_loads.append(len(lines))

        return offeted_loads

    def read_stats(self, services: List[Dict]) -> List[Dict]:
        service_statics = []
        for service_names in services:
            with open(self.artifacts + "response_" + service_names["name"] + ".txt","r") as file:
                lines = file.readlines()
            file.close()
            responses_from_node_1 = []
            responses_from_node_2 = []
            drops = []
            for line in lines:
                req = eval(line)
                if (req["code"] == 200):
                    if (req["Node"] == 1):
                        responses_from_node_1.append(req["response"])
                    elif (req["Node"] == 2):
                        responses_from_node_2.append(req["response"])
                else:
                    drops.append(req["response"])

            all_successful_response = responses_from_node_1 + responses_from_node_2
            cl1 = len(all_successful_response)
            if (len(responses_from_node_1) > 0):
                d11 = np.mean(responses_from_node_1)
                d11_std = np.std(responses_from_node_1)
            else:
                d11 = 0
                d11_std = 0

            if (len(responses_from_node_2) > 0):
                d12 = np.mean(responses_from_node_2)
                d12_std = np.std(responses_from_node_2)
            else:
                d12 = 0
                d12_std = 0

            if (len(all_successful_response) > 0):
                d1 = np.mean(all_successful_response)
                d1_99 = np.percentile(all_successful_response, 99)
                d1_90 = np.percentile(all_successful_response, 90)
                d1_std = np.std(all_successful_response)
            else:
                d1 = 0
                d1_99 = 0
                d1_90 = 0
                d1_std = 0

            drop1 = len(drops)
            statics = dict()
            statics["cl"] = cl1
            statics["d1"] = d11
            statics["d1_std"] = d11_std
            statics["d2"] = d12
            statics["d2_std"] = d12_std
            statics["d"] = d1
            statics["d_99"] = d1_99
            statics["d_90"] = d1_90
            statics["d_std"] = d1_std
            statics["drops"] = drop1
            service_statics.append(statics)
        return service_statics

    def collect_samples(self)  -> None:
        '''
        This funtion collect n sample from the testbed for the given service and configration of that service
        :param n: Number of samples
        :param services: A list of dictionaries of name of the service and its configration, the configuratoin
        includes p, b, c
        :return: None
        '''
        with open(self.artifacts + self.data_file_name, "a") as file:
            for i in range(self.n):
                self.cleanup_files(self.services)
                time.sleep(self.time_step)
                offered_loads = self.read_loads(self.services)
                statistics = self.read_stats(self.services)
                line = ""
                for i in range(len(self.services)):
                    line = (str(self.services[i]["l"]) + "," + str(offered_loads[i]) + "," + str(statistics[i]["cl"])
                            + "," + str(self.services[i]["p"])
                            + "," + str(self.services[i]["b"]) + "," + str(self.services[i]["c"]) + "," +
                            str(statistics[i]["d"]) + "," +  str(statistics[i]["d_std"]) + "," + str(statistics[i]["d1"])
                            + "," + str(statistics[i]["d1_std"]) + "," + str(statistics[i]["d2"]) + "," +
                            str(statistics[i]["d2_std"]) + "," +  str(statistics[i]["drops"]) + "\n")
                file.write(line)
        file.close()

    def collect_samples_k8(self) -> None:
        '''
                This funtion collect n sample from the testbed for the given service and configration of that service
                :param n: Number of samples
                :param services: A list of dictionaries of name of the service and its configration, the configuratoin
                includes p, b, c
                :return: None
                '''
        with open(self.artifacts + self.data_file_name, "a") as file:
            command_runner = RunCommandsOnCluster(self.path_to_config_files)
            for i in range(self.n):
                self.cleanup_files(self.services)
                time.sleep(self.time_step)
                offered_loads = self.read_loads(self.services)
                statistics = self.read_stats(self.services)
                (hpa, percentage) = command_runner.fetch_hap_replicas()
                line = ""
                for i in range(len(self.services)):
                    line = (str(self.services[i]["l"]) + "," + str(offered_loads[i]) + "," + str(statistics[i]["cl"])
                            + "," + str(self.services[i]["p"])
                            + "," + str(self.services[i]["b"]) + "," + str(self.services[i]["c"]) + "," +
                            str(statistics[i]["d"]) + "," + str(statistics[i]["d_std"]) + "," + str(statistics[i]["d1"])
                            + "," + str(statistics[i]["d1_std"]) + "," + str(statistics[i]["d2"]) + "," +
                            str(statistics[i]["d2_std"]) + "," + str(statistics[i]["drops"]) + "," + str(hpa)
                            + "," + str(percentage) + "\n")
                file.write(line)
        file.close()

    def collect_samples_noop(self) -> None:
        '''
                This funtion collect n sample from the testbed for the given service and configration of that service
                :param n: Number of samples
                :param services: A list of dictionaries of name of the service and its configration, the configuratoin
                includes p, b, c
                :return: None
                '''
        with open(self.artifacts + self.data_file_name, "a") as file:
            for i in range(self.n):
                self.cleanup_files(self.services)
                time.sleep(self.time_step)
                offered_loads = self.read_loads(self.services)
                statistics = self.read_stats(self.services)
                line = ""
                for i in range(len(self.services)):
                    line = (str(self.services[i]["l"]) + "," + str(offered_loads[i]) + "," + str(statistics[i]["cl"])
                            + "," + str(self.services[i]["p"])
                            + "," + str(self.services[i]["b"]) + "," + str(self.services[i]["c"]) + "," +
                            str(statistics[i]["d"]) + "," + str(statistics[i]["d_std"]) + "," + str(statistics[i]["d1"])
                            + "," + str(statistics[i]["d1_std"]) + "," + str(statistics[i]["d2"]) + "," +
                            str(statistics[i]["d2_std"]) + "," + str(statistics[i]["drops"]) + "\n")
                file.write(line)
        file.close()


    def apply_service_config(self) -> None:
        '''
        This function currently works only for one service since in the RunCommandsOnCluster paths are hard coded.
        Later we should add the name of the files for services so it can change the cofiguations for the services in the loop.
        :return:
        '''
        for service in self.services:
            routing_weight = service["p"]
            blocking_rate = service["b"]
            scaling = service["c"]
            command_runner = RunCommandsOnCluster(self.path_to_config_files)
            command_runner.set_routing_action(routing_weight)
            command_runner.set_scaling_action(scaling)
            command_runner.set_blocking_action(blocking_rate)
            command_runner.revise_routing_action()
            command_runner.run_routing_action()
            command_runner.revise_scaling_action()
            command_runner.run_scaling_action()
            command_runner.run_blocking_action(self.IP_port, service["name"])

    def data_collection(self) -> None:
        logging.info("====" + "The config is " + str(self.services[0]) + "====")
        self.apply_service_config()
        time.sleep(self.settling_time)
        self.collect_samples()

    def set_services(self, services) -> None:
        self.services = services
