class AdaptiveLearningOrchestrator:
    def __init__(self):
        self.learning_rate = 0.01
        self.performance_history = []

    def update_learning_rate(self):
        if len(self.performance_history) > 1:
            if self.performance_history[-1] > self.performance_history[-2]:
                self.learning_rate *= 1.1
            else:
                self.learning_rate *= 0.9

    def train_iteration(self, model, data):
        performance = model.train(data, learning_rate=self.learning_rate)
        self.performance_history.append(performance)
        self.update_learning_rate()
        return performance

    def orchestrate_training(self, model, data, iterations):
        for _ in range(iterations):
            performance = self.train_iteration(model, data)
            yield performance

alo = AdaptiveLearningOrchestrator()
