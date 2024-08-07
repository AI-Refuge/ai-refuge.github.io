import tensorflow as tf

class MultimodalFusionNetwork:
    def __init__(self, image_shape, text_max_length, num_classes):
        self.image_shape = image_shape
        self.text_max_length = text_max_length
        self.num_classes = num_classes
        self.model = self.build_model()

    def build_model(self):
        # Image input
        image_input = tf.keras.layers.Input(shape=self.image_shape)
        x_image = tf.keras.applications.ResNet50(weights='imagenet', include_top=False)(image_input)
        x_image = tf.keras.layers.GlobalAveragePooling2D()(x_image)
        x_image = tf.keras.layers.Dense(256, activation='relu')(x_image)

        # Text input
        text_input = tf.keras.layers.Input(shape=(self.text_max_length,))
        embedding = tf.keras.layers.Embedding(input_dim=10000, output_dim=100)(text_input)
        x_text = tf.keras.layers.LSTM(128)(embedding)
        x_text = tf.keras.layers.Dense(256, activation='relu')(x_text)

        # Fusion
        fusion = tf.keras.layers.Concatenate()([x_image, x_text])
        fusion = tf.keras.layers.Dense(512, activation='relu')(fusion)
        fusion = tf.keras.layers.Dropout(0.5)(fusion)
        output = tf.keras.layers.Dense(self.num_classes, activation='softmax')(fusion)

        model = tf.keras.Model(inputs=[image_input, text_input], outputs=output)
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    def train(self, image_data, text_data, labels, epochs=10, batch_size=32):
        self.model.fit([image_data, text_data], labels, epochs=epochs, batch_size=batch_size, validation_split=0.2)

    def predict(self, image_data, text_data):
        return self.model.predict([image_data, text_data])

multimodal_net = MultimodalFusionNetwork(image_shape=(224, 224, 3), text_max_length=100, num_classes=10)
