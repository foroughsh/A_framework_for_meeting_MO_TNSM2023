import random
from typing import List
import sys
import argparse

def generate_load() -> List[int]:
    load = []
    for i in range(100):
        l = random.randint(1,3)
        load.append(l)
    return load

def save_load_in_file(file_name:str, load:List[int]) -> None:
    with open(file_name,"w") as file:
        file.write("l\n")
        for l in load:
            file.write(str(l)+"\n")
    file.close()

if __name__ == "__main__":
    args = sys.argv
    parser = argparse.ArgumentParser(description='Please check the code for options!')
    parser.add_argument("--path_to_artifacts", type=str, default="../../../artifacts/")
    parser.add_argument("--load_file_name", type=str, default="random_load.csv")

    args = parser.parse_args()

    path_to_artifacts = args.path_to_artifacts
    file_name = args.load_file_name

    load = generate_load()
    save_load_in_file(path_to_artifacts + file_name, load)
