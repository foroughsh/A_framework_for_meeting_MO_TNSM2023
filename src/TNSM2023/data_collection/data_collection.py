import random
import numpy as np
import joblib
import paramiko
import subprocess
import time
import requests
import sys
import os
from pathlib import Path
from typing import List
from TNSM2023.data_collection.run_commands_on_cluster import RunCommandsOnCluster

class DataCollection:
    def __init__(self, IP_port:str, path_to_save_data:str, path_to_artifacts:str, path_to_LG:str, time_step:int = 5) -> None:
        self.IP_port = IP_port
        self.artifacts = path_to_artifacts
        self.time_step = time_step
        self.path_to_save_data = path_to_save_data
        self.path_to_LG = path_to_LG

    def run_load_generator(self, LG_name:str, load_value:float) -> None:
        # Define the shell command to run
        shell_cmd = "nohup python " + self.path_to_LG + "async_load_generator.py " + LG_name + " constant " + str(
            load_value) + " " + self.IP_port + " > /dev/null &"

        # Run the command in the background
        subprocess.Popen(shell_cmd, shell=True)

    def kill_load_generator(self) -> None:
        # Define the shell command to run
        shell_cmd = "pkill -f async_load_generator.py"

        # Run the command in the background
        subprocess.Popen(shell_cmd, shell=True)

    def get_load_pattern(self, file_name:str) -> List[float]:
        with open(file_name) as file:
            lines = file.readlines
        file.close()
        load_pattern = []
        for line in lines:
            load_pattern.append(float(line))
        return load_pattern
