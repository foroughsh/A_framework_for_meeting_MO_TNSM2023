import pandas as pd
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
from typing import List
import numpy as np

class SystemModel:

    def __init__(self, number_of_estimators:int=120, data_file_name:str="data.csv", artifacts:str="../../../artifacts/") -> None:
        self.data_file_name = data_file_name
        self.artifacts = artifacts
        self.number_of_estimators = number_of_estimators
        self.model = RandomForestRegressor(n_estimators=self.number_of_estimators)

    def learn_system_model(self, x_features:List[str], y_features:List[str], test_size:float=0.05,
                           save_predicitons_and_ys="False"):
        data = pd.read_csv(self.artifacts + self.data_file_name)

        train, test = train_test_split(data, test_size=test_size)

        train = train.sort_index(axis=0)
        test = test.sort_index(axis=0)
        X_train = train[x_features].iloc[1:]
        X_test = test[x_features].iloc[1:]
        Y_train = train[y_features].iloc[1:]
        Y_test = test[y_features].iloc[1:]

        self.model.fit(X_train.values, Y_train)

        pred_test = self.model.predict(X_test)
        predict_test = (np.array(pred_test)).reshape(pred_test.shape[0], Y_test.shape[1])

        pred_train = self.model.predict(X_train)
        predict_train = (np.array(pred_train)).reshape(pred_train.shape[0], Y_test.shape[1])

        if save_predicitons_and_ys:
            df_test_ys_prediciton = pd.DataFrame([Y_test,predict_test])
            df_test_ys_prediciton.to_csv(self.artifacts + "test_predicitons.csv", index=False)

        test_nmae, train_nmae, test_r2score, train_r2score, avg_error = self.test_train_nmae_r2score(predict_test, predict_train,
                                                                                     Y_test,
                                                                                     Y_train)
        return test_nmae, train_nmae, test_r2score, train_r2score, avg_error

    def test_train_nmae_r2score(self, test_predicted_values, train_predicted_values, test_set, train_set):
        col_size = train_set.shape[1]
        test_nmaes = []
        train_names = []
        test_r2s = []
        train_r2s = []
        avg_erro = []
        for i in range(col_size):
            diff_test = np.abs(test_predicted_values[:, i] - test_set.iloc[:, i])
            test_nmae = (diff_test.mean()) / test_set.iloc[:, i].mean()
            test_r2score = r2_score(test_set.iloc[:, i], test_predicted_values[:, i])
            diff_train = np.abs(train_predicted_values[:, i] - train_set.iloc[:, i])
            train_nmae = (diff_train.mean()) / train_set.iloc[:, i].mean()
            train_r2score = r2_score(train_set.iloc[:, i], train_predicted_values[:, i])
            test_nmaes.append(test_nmae)
            train_names.append(train_nmae)
            test_r2s.append(test_r2score)
            train_r2s.append(train_r2score)
            avg_erro.append(test_nmae * test_set.iloc[:, i].mean())
        return test_nmaes, train_names, test_r2s, train_r2s, avg_erro

    def save_model(self, target_file_name):
        joblib.dump(self.model, self.artifacts + target_file_name + ".joblib")

    def load_model(self, model_name):
        joblib.load(self.artifacts + model_name)

    # def generate_predicitons_using_the_model(self, controls:List[List[float]], file_name) -> None:
    #     for control in controls:
    #         for value in control:

