import sys
import argparse
import joblib

def reward_function(d1:float, c:int, O1:float=1):
    d1 = round(d1, 3) + 0.4
    reward = 0
    if (d1 <= O1):
        reward = 6 - c
    else:
        if (d1 > O1):
            reward = O1 - d1
    return round(reward, 3)

if __name__ == "__main__":
    args = sys.argv

    parser = argparse.ArgumentParser(description='Please check the code for options!')
    parser.add_argument("--file_name", type=str, default="optimal_policy.csv")
    parser.add_argument("--artifacts", type=str, default="../../../artifacts/")
    parser.add_argument("--system_model", type=str, default="system_model.joblib")


    args = parser.parse_args()

    file_name = args.file_name
    artifacts = args.artifacts
    system_model = args.system_model

    system_model_path = artifacts + system_model
    delay_models = joblib.load(system_model_path)

    with open(artifacts + file_name, "w") as file:
        file.write("l,r,p,c,d\n")
        for l in [4, 8, 12]:
            max_reward = -1000
            best_p = 0
            best_c = 0
            best_d = 0
            for c in [1, 2, 3, 4, 5]:
                for p in [0, 0.2, 0.4, 0.6, 0.8, 1]:
                    [d1] = delay_models.predict([[l, l * 5, l * 5, p * 100, l, c]])
                    reward = reward_function(d1, c)
                    if reward>max_reward:
                        max_reward = reward
                        best_p = p
                        best_c = c
                        best_d = d1
            line = str(l) + "," + str(max_reward) + "," + str(best_p) + "," + str(best_c) + "," + str(best_d) + "\n"
            print(line)
            file.write(line)
    file.close()




