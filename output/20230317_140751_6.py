import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Load historical data
def load_data(csv_file):
    df = pd.read_csv(csv_file, parse_dates=['Date'], index_col='Date')
    return df

# Preprocess the data
def preprocess_data(df):
    dataset = df['Close']
    dataset = dataset.values.reshape(-1, 1)
    scaler = MinMaxScaler()
    dataset = scaler.fit_transform(dataset)

    return dataset, scaler

def create_training_data(dataset, lookback=60):
    X = []
    y = []

    for i in range(lookback, len(dataset)):
        X.append(dataset[i-lookback:i, 0])
        y.append(dataset[i, 0])

    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    return X, y

# Build the LSTM model
def build_lstm_model(lookback):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(lookback, 1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_squared_error')

    return model

# Train and evaluate the model
def train_evaluate_model(model, X_train, y_train, X_test, y_test, scaler):
    model.fit(X_train, y_train, batch_size=1, epochs=5, verbose=0)

    # Make predictions
    predictions = model.predict(X_test)
    predictions = scaler.inverse_transform(predictions)
    actual = scaler.inverse_transform(y_test.reshape(-1, 1))

    plt.plot(predictions, label='Predictions')
    plt.plot(actual, label='Actual')
    plt.legend()
    plt.show()

def main():
    csv_file = 'ETH-USD.csv'  # Replace with the path to your downloaded historical data file
    df = load_data(csv_file)
    dataset, scaler = preprocess_data(df)
    
    lookback = 60
    X, y = create_training_data(dataset, lookback)
    split_index = int(0.8 * len(X))
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]

    model = build_lstm_model(lookback)
    
    train_evaluate_model(model, X_train, y_train, X_test, y_test, scaler)
    
    #print the model summary
    print(model.summary())

if __name__ == '__main__':
    main()