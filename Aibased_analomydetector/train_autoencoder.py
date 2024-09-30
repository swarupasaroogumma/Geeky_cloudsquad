import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
import numpy as np

def create_autoencoder(input_dim):
    """Create and compile an autoencoder model."""
    input_layer = Input(shape=(input_dim,))
    encoded = Dense(32, activation='relu')(input_layer)
    encoded = Dense(16, activation='relu')(encoded)
    decoded = Dense(32, activation='relu')(encoded)
    decoded = Dense(input_dim, activation='sigmoid')(decoded)

    autoencoder = Model(input_layer, decoded)
    autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
    return autoencoder

def generate_synthetic_traffic_data(num_samples, input_dim):
    """Generate synthetic traffic data for training."""
    return np.random.rand(num_samples, input_dim)

def main():
    """Main function to train and save the autoencoder model."""
    input_dim = 20  
    x_train = generate_synthetic_traffic_data(1000, input_dim)  

    autoencoder = create_autoencoder(input_dim)
    autoencoder.fit(x_train, x_train,
                    epochs=50,
                    batch_size=256,
                    validation_split=0.1,
                    shuffle=True)

    autoencoder.save('autoencoder_model.h5')
    print("Autoencoder model saved as 'autoencoder_model.h5'")

if __name__ == '__main__':
    main()
