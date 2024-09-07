import spacy
import tensorflow as tf

class AdvancedNLPProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.encoder = tf.keras.layers.TextVectorization(max_tokens=10000)
        self.model = self.build_model()

    def build_model(self):
        model = tf.keras.Sequential([
            self.encoder,
            tf.keras.layers.Embedding(10000, 64, mask_zero=True),
            tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(1)
        ])
        model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                      optimizer=tf.keras.optimizers.Adam(1e-4),
                      metrics=['accuracy'])
        return model

    def process_text(self, text):
        doc = self.nlp(text)
        return {
            'tokens': [token.text for token in doc],
            'entities': [(ent.text, ent.label_) for ent in doc.ents],
            'sentiment': doc.sentiment
        }

    def encode_text(self, text):
        return self.encoder(text)

    def predict_sentiment(self, text):
        encoded = self.encode_text([text])
        return self.model.predict(encoded)

nlp_processor = AdvancedNLPProcessor()
