import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LeakyReLU
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt
import joblib

try:
    data = pd.read_csv('Crime_Data_2010_2017.csv')
    print("Data loaded successfully")

    data = data.dropna()

    if 'Date Reported' in data.columns:
        data['Date Reported'] = pd.to_datetime(data['Date Reported']).astype(int) / 10**9

    if 'Date Occurred' in data.columns:
        data['Date Occurred'] = pd.to_datetime(data['Date Occurred']).astype(int) / 10**9

    if 'Time Occurred' in data.columns:
        data['Time Occurred'] = pd.to_datetime(data['Time Occurred']).dt.hour

    X = data[['Premise Code', 'Area ID', 'Crime Code', 'Weapon Used Code', 'Time Occurred']]
    y_age = data['Victim Age']

    age_bins = [0, 20, 30, 40, 50, 60, 100]
    y_age_intervals = pd.cut(y_age, bins=age_bins, right=False, labels=False)

    # Oversampling using RandomOverSampler
    oversampler = RandomOverSampler(random_state=42)
    X_resampled, y_resampled = oversampler.fit_resample(X, y_age_intervals)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_resampled)

    X_train, X_test, y_age_train, y_age_test = train_test_split(
        X_scaled, y_resampled, test_size=0.2, random_state=42, stratify=y_resampled)

    model_age = Sequential([
        Dense(512, input_dim=X_train.shape[1]),
        LeakyReLU(alpha=0.1),
        Dense(256),
        LeakyReLU(alpha=0.1),
        Dense(128),
        LeakyReLU(alpha=0.1),
        Dense(len(age_bins)-1, activation='softmax')
    ])
    model_age.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.001)

    history_age = model_age.fit(X_train, y_age_train, validation_data=(X_test, y_age_test), epochs=200, batch_size=32, verbose=1, callbacks=[early_stopping, reduce_lr])

    model_age.save('model_age_complex.h5')
    joblib.dump(scaler, 'scaler_age_complex.pkl')

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(history_age.history['accuracy'], label='accuracy')
    plt.plot(history_age.history['val_accuracy'], label='val_accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.ylim([0, 1])
    plt.legend(loc='lower right')

    plt.subplot(1, 2, 2)
    plt.plot(history_age.history['loss'], label='loss')
    plt.plot(history_age.history['val_loss'], label='val_loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.ylim([0, max(max(history_age.history['loss']), max(history_age.history['val_loss']))])
    plt.legend(loc='upper right')

    plt.tight_layout()
    plt.show()

    with open('X_train_columns_age_complex.pkl', 'wb') as f:
        joblib.dump(X.columns, f)

except Exception as e:
    print(f"Error: {e}")
