import tensorflow as tf
import tensorflow_federated as tff

class FederatedLearningSystem:
    def __init__(self, model_fn):
        self.model_fn = model_fn
        self.client_data = None
        self.federated_algorithm = None

    def preprocess_data(self, dataset):
        def batch_format_fn(element):
            return collections.OrderedDict(
                x=tf.reshape(element['x'], [-1, 784]),
                y=tf.reshape(element['y'], [-1, 1]))
        return dataset.repeat(NUM_EPOCHS).shuffle(SHUFFLE_BUFFER).batch(
            BATCH_SIZE).map(batch_format_fn).prefetch(PREFETCH_BUFFER)

    def initialize_federated_learning(self):
        sample_client_data = self.preprocess_data(self.client_data[0])
        def client_data_fn():
            return [self.preprocess_data(cd) for cd in self.client_data]
        
        federated_train_data = tff.simulation.ClientData.from_clients_and_fn(
            client_ids=[str(i) for i in range(len(self.client_data))],
            create_tf_dataset_for_client_fn=client_data_fn)
        
        self.federated_algorithm = tff.learning.build_federated_averaging_process(
            self.model_fn,
            client_optimizer_fn=lambda: tf.keras.optimizers.SGD(learning_rate=0.02),
            server_optimizer_fn=lambda: tf.keras.optimizers.SGD(learning_rate=1.0))

    def train_round(self):
        state = self.federated_algorithm.initialize()
        for round_num in range(NUM_ROUNDS):
            state, metrics = self.federated_algorithm.next(state, federated_train_data)
            print(f'Round {round_num}')
            print(metrics)

federated_system = FederatedLearningSystem(model_fn=create_keras_model)
