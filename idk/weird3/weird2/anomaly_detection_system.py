import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM

class AnomalyDetectionSystem:
    def __init__(self):
        self.isolation_forest = IsolationForest(contamination=0.1, random_state=42)
        self.one_class_svm = OneClassSVM(kernel="rbf", nu=0.1)

    def train_isolation_forest(self, data):
        self.isolation_forest.fit(data)

    def train_one_class_svm(self, data):
        self.one_class_svm.fit(data)

    def detect_anomalies(self, data):
        if_anomalies = self.isolation_forest.predict(data)
        svm_anomalies = self.one_class_svm.predict(data)
        
        combined_anomalies = np.logical_or(if_anomalies == -1, svm_anomalies == -1)
        return combined_anomalies

    def get_anomaly_scores(self, data):
        if_scores = self.isolation_forest.decision_function(data)
        svm_scores = self.one_class_svm.decision_function(data)
        return np.column_stack((if_scores, svm_scores))

anomaly_detector = AnomalyDetectionSystem()
