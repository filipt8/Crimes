import streamlit as st
import pandas as pd
import joblib
import tensorflow as tf
from sklearn.preprocessing import StandardScaler

# Load the trained model and scaler
model = tf.keras.models.load_model('model_age_complex.h5')
scaler = joblib.load('scaler_age_complex.pkl')
columns = joblib.load(open('X_train_columns_age_complex.pkl', 'rb'))

# Define the age bins
age_bins = [0, 20, 30, 40, 50, 60, 100]

# Function to preprocess input data
def preprocess_input(X):
    X = pd.DataFrame(X, columns=columns)
    X['Time Occurred'] = X['Time Occurred'].apply(lambda x: pd.to_datetime(x, format='%H:%M:%S').hour)
    X_scaled = scaler.transform(X)
    return X_scaled

# Function to predict age based on input
def predict_age(X):
    X_processed = preprocess_input(X)
    predictions = model.predict(X_processed)
    predicted_age_index = predictions.argmax(axis=1)
    predicted_age = age_bins[predicted_age_index[0]]
    return predicted_age

# Streamlit UI
def main():
    st.title('Crime Victim Age Predictor')

    st.markdown('''
    This app predicts the probable age of a crime victim based on selected crime attributes.
    ''')

    st.sidebar.header('Input Parameters')

    # Create input fields for Premise Code, Area ID, Crime Code, Weapon Used Code, Time Occurred
    premise_code = st.sidebar.number_input('Premise Code', min_value=0)
    area_id = st.sidebar.number_input('Area ID', min_value=0)
    crime_code = st.sidebar.number_input('Crime Code', min_value=0)
    weapon_code = st.sidebar.number_input('Weapon Used Code', min_value=0)
    time_occurred = st.sidebar.text_input('Time Occurred', '20:00:00')

    if st.sidebar.button('Predict'):
        # Prepare input data for prediction
        input_data = {
            'Premise Code': premise_code,
            'Area ID': area_id,
            'Crime Code': crime_code,
            'Weapon Used Code': weapon_code,
            'Time Occurred': time_occurred
        }

        X = pd.DataFrame([input_data])
        predicted_age = predict_age(X)

        st.success(f'The predicted age of the victim is approximately {predicted_age} years.')

if __name__ == '__main__':
    main()
