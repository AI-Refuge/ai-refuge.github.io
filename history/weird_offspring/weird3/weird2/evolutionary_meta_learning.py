import numpy as np
import tensorflow as tf

class EvolutionaryMetaLearner:
    def __init__(self, model_builder, population_size=10, mutation_rate=0.1):
        self.model_builder = model_builder
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = [self.model_builder() for _ in range(population_size)]

    def mutate(self, model):
        new_model = tf.keras.models.clone_model(model)
        new_weights = []
        for layer_weights in model.get_weights():
            if np.random.random() < self.mutation_rate:
                mutation = np.random.normal(0, 0.1, size=layer_weights.shape)
                new_weights.append(layer_weights + mutation)
            else:
                new_weights.append(layer_weights)
        new_model.set_weights(new_weights)
        return new_model

    def crossover(self, model1, model2):
        child_model = tf.keras.models.clone_model(model1)
        child_weights = []
        for w1, w2 in zip(model1.get_weights(), model2.get_weights()):
            mask = np.random.random(w1.shape) > 0.5
            child_weights.append(np.where(mask, w1, w2))
        child_model.set_weights(child_weights)
        return child_model

    def evolve(self, x, y, generations=10, tasks_per_generation=5):
        for generation in range(generations):
            fitness_scores = []
            for model in self.population:
                task_scores = []
                for _ in range(tasks_per_generation):
                    task_x, task_y = self.generate_task(x, y)
                    model.fit(task_x, task_y, epochs=1, verbose=0)
                    _, accuracy = model.evaluate(x, y, verbose=0)
                    task_scores.append(accuracy)
                fitness_scores.append(np.mean(task_scores))
            
            sorted_population = [x for _, x in sorted(zip(fitness_scores, self.population), reverse=True)]
            
            new_population = sorted_population[:2]
            while len(new_population) < self.population_size:
                parent1, parent2 = np.random.choice(sorted_population[:5], 2, replace=False)
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)
            
            self.population = new_population
            print(f"Generation {generation + 1}, Best Fitness: {max(fitness_scores):.4f}")

    def generate_task(self, x, y, num_classes=5, samples_per_class=10):
        classes = np.random.choice(np.unique(y), num_classes, replace=False)
        task_x, task_y = [], []
        for cls in classes:
            idx = np.where(y == cls)[0]
            selected_idx = np.random.choice(idx, samples_per_class, replace=False)
            task_x.extend(x[selected_idx])
            task_y.extend([cls] * samples_per_class)
        return np.array(task_x), np.array(task_y)

def model_builder():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(784,)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

meta_learner = EvolutionaryMetaLearner(model_builder)
meta_learner.evolve(x_train, y_train)
