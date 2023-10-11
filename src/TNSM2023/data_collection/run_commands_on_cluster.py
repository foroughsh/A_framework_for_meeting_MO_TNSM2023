import logging
import fileinput
import sys
import subprocess

class RunCommandsOnCluster:
    """
    The class RunCommandsOnCluster includes all functions to revise the configuration files and run them on the cluster
    """

    def __init__(self) -> None:
        """Initialize a RunCommandsOnCluster instance."""
        logging.info(f"Running command object is successfully generated!")
        self.configurations_path = "../../cluster_configuration_files/"
        self.routing_file = "routing.yaml"
        self.scaling_file = "scaling.yaml"
        self.routing_action = 50
        self.scaling_action = 1000

    def set_routing_action(self, routing_action: int) -> None:
        '''
        This function sets the routing action
        :param routing_action: The routing weight
        :return: None
        '''
        if (routing_action>=0) and (routing_action<=100):
            self.routing_action = routing_action

    def get_routing_action(self) -> int:
        '''
        This funtion returns the routing action
        :return: routing action
        '''
        return self.routing_action

    def set_scaling_action(self, scaling_action: int) -> None:
        '''
        This function sets the scaling action
        :param scaling_action: The scaling weight
        :return: None
        '''
        self.scaling_action = scaling_action

    def get_scaling_action(self) -> int:
        '''
        This funtion returns the scaling action
        :return: scaling action
        '''
        return self.scaling_action

    def revise_scaling_action(self) -> None:
        '''
        This function revise the scaling configuration file
        :return: None
        '''
        for line in fileinput.input(self.configurations_path + self.scaling_file, inplace=True):
            if ("replicas:" in line):
                line = line.replace(line, '  replicas: ' + str(self.scaling_action)) + "\n"
            sys.stdout.write(line)

    def run_scaling_action(self) -> int:
        '''
        This function runs the configuration file on the cluster to change the number of replicas
        :return: 0 if there is no error, 1 if an error happens
        '''
        command = "kubectl apply -f " + self.configurations_path + self.scaling_file

        # Use subprocess to run the command
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check the result
        if result.returncode == 0:
            logging.info(result.stdout)
            return 0
        else:
            logging.info(result.stderr)
            return 1

    def revise_routing_action(self) -> None:
        '''
        This function revise the configuration file for the routing
        :return:
        '''
        counter = 0
        for line in fileinput.input(self.configurations_path + self.routing_file, inplace=True):
            if ("weight:" in line):
                if (counter == 0):
                    line = line.replace(line, "      weight: " + str(self.routing_action)) + "\n"
                    counter += 1
                elif (counter == 1):
                    line = line.replace(line, "      weight: " + str(100 - self.routing_action)) + "\n"
                    counter += 1
            sys.stdout.write(line)