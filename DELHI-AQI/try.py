import streamlit as st
import pandas as pd
import pickle

# Load model and label encoder
with open("aqi_model.pkl", "rb") as f:
    model, label_encoder = pickle.load(f)

# Load the dataset to access station-to-zone mapping
df = pd.read_csv("data.csv")

# Create a station-to-zone mapping
station_to_zone = dict(zip(df['Station'], df['Zone']))

st.title("AQI Prediction App")

# Station selection
st.sidebar.header("Input Details")
station = st.sidebar.selectbox("Select Station", options=sorted(station_to_zone.keys()))
zone = station_to_zone[station]  # Automatically fetch the zone based on the selected station

st.sidebar.markdown(f"**Zone:** {zone}")

# Environmental inputs
ozone = st.sidebar.number_input("Ozone Level", min_value=0.0, step=0.1)
co = st.sidebar.number_input("CO Level", min_value=0.0, step=0.1)
so2 = st.sidebar.number_input("SO2 Level", min_value=0.0, step=0.1)
no2 = st.sidebar.number_input("NO2 Level", min_value=0.0, step=0.1)
pm10 = st.sidebar.number_input("PM10 Level", min_value=0.0, step=0.1)
pm25 = st.sidebar.number_input("PM2.5 Level", min_value=0.0, step=0.1)

# Prediction
if st.sidebar.button("Predict AQI Category"):
    features = pd.DataFrame([[ozone, co, so2, no2, pm10, pm25]], 
                            columns=['Ozone', 'CO', 'SO2', 'NO2', 'PM10', 'PM2.5'])
    prediction = model.predict(features)[0]
    category = label_encoder.inverse_transform([prediction])[0]
    st.success(f"The predicted AQI Category is: **{category}**")
    
# Display suggestions based on AQI Category
    st.markdown("### Suggestions")
    if category == "Good":
        st.write("✅ *Air quality is good.* You can enjoy outdoor activities without any concerns.")
    elif category == "Moderate":
        st.write("⚠️ *Air quality is moderate.* Sensitive individuals should limit prolonged outdoor activities.")
    elif category == "Unhealthy for Sensitive Groups":
        st.write("😷 *Air quality is unhealthy for sensitive groups.* People with respiratory or heart conditions should reduce outdoor exertion.")
    elif category == "Unhealthy":
        st.write("🚨 *Air quality is unhealthy.* Everyone should reduce outdoor activities, especially children and older adults.")
    elif category == "Very Unhealthy":
        st.write("❗ *Air quality is very unhealthy.* Avoid outdoor activities. Use air purifiers indoors.")
    elif category == "Hazardous":
        st.write("🛑 *Air quality is hazardous.* Stay indoors and use high-quality air filtration systems. Avoid all outdoor activities.")

# Optional: Display selected

# Optional: Display selected details
st.markdown("### Selected Details")
st.write(f"**Station:** {station}")
st.write(f"**Zone:** {zone}")
st.write(f"**Ozone Level:** {ozone}")
st.write(f"**CO Level:** {co}")
st.write(f"**SO2 Level:** {so2}")
st.write(f"**NO2 Level:** {no2}")
st.write(f"**PM10 Level:** {pm10}")
st.write(f"**PM2.5 Level:** {pm25}")
