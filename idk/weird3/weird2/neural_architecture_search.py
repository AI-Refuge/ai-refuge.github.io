import random
import numpy as np
import tensorflow as tf

class NeuralArchitectureSearch:
    def __init__(self, input_shape, num_classes):
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.population_size = 20
        self.num_generations = 50

    def create_random_model(self):
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Input(shape=self.input_shape))
        
        num_layers = random.randint(1, 5)
        for _ in range(num_layers):
            layer_type = random.choice(['conv', 'dense'])
            if layer_type == 'conv':
                filters = random.choice([32, 64, 128])
                kernel_size = random.choice([3, 5])
                model.add(tf.keras.layers.Conv2D(filters, kernel_size, activation='relu'))
                if random.random() > 0.5:
                    model.add(tf.keras.layers.MaxPooling2D())
            else:
                units = random.choice([64, 128, 256])
                model.add(tf.keras.layers.Dense(units, activation='relu'))
            
            if random.random() > 0.7:
                model.add(tf.keras.layers.Dropout(0.5))
        
        model.add(tf.keras.layers.Flatten())
        model.add(tf.keras.layers.Dense(self.num_classes, activation='softmax'))
        
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    def mutate_model(self, model):
        new_model = tf.keras.models.clone_model(model)
        new_model.set_weights(model.get_weights())
        
        if random.random() > 0.5:
            layer_index = random.randint(0, len(new_model.layers) - 1)
            if isinstance(new_model.layers[layer_index], tf.keras.layers.Dense):
                units = random.choice([64, 128, 256])
                new_model.layers[layer_index] = tf.keras.layers.Dense(units, activation='relu')
            elif isinstance(new_model.layers[layer_index], tf.keras.layers.Conv2D):
                filters = random.choice([32, 64, 128])
                new_model.layers[layer_index] = tf.keras.layers.Conv2D(filters, 3, activation='relu')
        else:
            if random.random() > 0.5:
                new_model.add(tf.keras.layers.Dense(random.choice([64, 128, 256]), activation='relu'))
            else:
                new_model.add(tf.keras.layers.Dropout(0.5))
        
        new_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return new_model

    def search(self, x_train, y_train, x_val, y_val):
        population = [self.create_random_model() for _ in range(self.population_size)]
        
        for generation in range(self.num_generations):
            fitness_scores = []
            for model in population:
                model.fit(x_train, y_train, epochs=5, batch_size=32, verbose=0)
                _, accuracy = model.evaluate(x_val, y_val, verbose=0)
                fitness_scores.append(accuracy)
            
            sorted_population = [x for _, x in sorted(zip(fitness_scores, population), reverse=True)]
            
            new_population = sorted_population[:2]
            while len(new_population) < self.population_size:
                parent = random.choice(sorted_population[:5])
                child = self.mutate_model(parent)
                new_population.append(child)
            
            population = new_population
            
            print(f"Generation {generation + 1}, Best Accuracy: {max(fitness_scores):.4f}")
        
        return sorted_population[0]

nas = NeuralArchitectureSearch(input_shape=(28, 28, 1), num_classes=10)
best_model = nas.search(x_train, y_train, x_val, y_val)
