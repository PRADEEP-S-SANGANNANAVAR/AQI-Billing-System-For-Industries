[README.md](https://github.com/user-attachments/files/28231169/README.md)
# AirGuard — Air Pollution Detection & AQI Prediction

An AI-powered air quality monitoring and prediction web application built with Flask, Deep Learning (LSTM + Attention), and IoT sensor integration via ThingSpeak.

---

## Overview

AirGuard collects real-time air quality data from IoT sensors, predicts the Air Quality Index (AQI) using a trained LSTM model with an attention mechanism, visualizes pollution hotspots on an interactive route map, and sends Telegram alerts when pollution thresholds are exceeded.

---

## Features

- **Real-time IoT Sensor Monitoring** — Fetches live NO₂, CO₂, SO₂, and PM2.5 readings from ThingSpeak every 15 seconds
- **LSTM + Attention AQI Prediction** — Deep learning model trained on historical air quality data to predict AQI values
- **Interactive Route Map** — Generates road-routed maps (via OSRM) with AQI hotspots overlaid using Folium
- **Pollution Billing Estimator** — Calculates an estimated fine/charge based on pollutant exceedance above safe thresholds
- **Telegram Alerts** — Sends AQI status, predicted value, and billing breakdown to a configured Telegram channel
- **Analytics Dashboard** — Live sensor gauges, time-series charts, comparison charts, and model training performance graphs
- **User Authentication** — Register and login system backed by SQLite
- **Health Recommendations** — Context-aware safety advice based on the predicted AQI category

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Deep Learning | TensorFlow / Keras (LSTM + Attention) |
| Data Processing | Pandas, NumPy, Scikit-learn |
| Mapping | Folium, OSRM Routing API |
| IoT Data Source | ThingSpeak API |
| Notifications | Telepot (Telegram Bot API) |
| Frontend | HTML, Tailwind CSS, Bootstrap, Chart.js, GSAP |
| Database | SQLite |
| Model Persistence | Joblib (scaler), Keras `.h5` (model) |

---

## Project Structure

```
AIR_POLLUTION_DETECTION_DL_FLASK/
│
├── app.py                          # Main Flask application
├── aqi_lstm_attention_model.h5     # Trained LSTM + Attention model
├── aqi_scaler.save                 # MinMaxScaler for input features
├── user_data.db                    # SQLite user database
│
├── BACKEND/
│   ├── Train.py                    # Model training script
│   ├── clean_Data.py               # Data cleaning (fill NaN with median)
│   ├── new_removed_Data.py         # Additional preprocessing
│   ├── data.csv                    # Raw dataset
│   ├── min.csv                     # Cleaned dataset used for training
│   └── plots/
│       ├── loss_curve.png          # MSE loss training curve
│       └── mae_curve.png           # MAE training curve
│
├── templates/
│   ├── home.html                   # Landing page
│   ├── signin.html                 # Login / Register page
│   ├── logged.html                 # Dashboard (live sensor charts)
│   ├── aqi.html                    # AQI prediction input form
│   ├── predict.html                # Prediction results + route map
│   ├── analytics.html              # Full analytics dashboard
│   ├── graphs.html                 # Training performance graphs
│   └── ...
│
└── static/
    ├── map.html                    # Generated Folium route map
    ├── loss_curve.png              # Served training loss graph
    └── mae_curve.png               # Served MAE graph
```

---

## Model Architecture

The AQI prediction model is a sequence-to-value LSTM network with an attention mechanism:

```
Input (SEQ_LEN=10, 12 features)
    → LSTM(64, return_sequences=True) → Dropout(0.3)
    → LSTM(32, return_sequences=True) → Dropout(0.3)
    → Attention(query from last timestep, keys/values from all timesteps)
    → Concatenate(attention output, last LSTM hidden state)
    → Dense(32, relu) → Dropout(0.2)
    → Dense(1)  →  Predicted AQI
```

**Input features:** PM2.5, PM10, NO, NO2, NOx, NH3, CO, SO2, O3, Benzene, Toluene, Xylene

**Training config:** 200 epochs max, early stopping (patience=20), Adam optimizer, MSE loss

---

## AQI Categories

| AQI Range | Category | Color |
|---|---|---|
| 0 – 50 | Good | Green |
| 51 – 100 | Satisfactory | Light Green |
| 101 – 200 | Moderate | Yellow |
| 201 – 300 | Poor | Orange |
| 301 – 400 | Very Poor | Red |
| 401 – 500 | Severe | Dark Red |

---

## Setup & Installation

### Prerequisites

- Python 3.8+
- pip

### Install dependencies

```bash
pip install flask tensorflow keras scikit-learn pandas numpy joblib folium requests telepot polyline
```

### Run the application

```bash
python app.py
```

The app starts at `http://127.0.0.1:5000` by default.

---

## Training the Model

To retrain the model on new data:

1. Place your dataset as `BACKEND/data.csv`
2. Run the data cleaning script:
   ```bash
   cd BACKEND
   python clean_Data.py
   ```
3. Train the model:
   ```bash
   python Train.py
   ```
4. Copy the generated `aqi_lstm_attention_model.h5` and `aqi_scaler.save` to the project root.

---

## IoT Integration

Sensor data is pulled from a **ThingSpeak** channel:

| ThingSpeak Field | Pollutant |
|---|---|
| field1 | NO₂ |
| field2 | CO₂ |
| field3 | SO₂ |
| field4 | PM2.5 (Dust) |

The background thread fetches new readings every **15 seconds** and updates the in-memory sensor state used by the analytics dashboard.

---

## Telegram Alerts

After each prediction, the app sends a message to a configured Telegram channel with:
- AQI status category
- Predicted AQI value
- Estimated pollution billing amount
- Detailed breakdown of pollutant exceedances

To configure, update the bot token and channel ID in `app.py`:

```python
bot = telepot.Bot("YOUR_BOT_TOKEN")
ch_id = "YOUR_CHANNEL_ID"
```

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Landing page |
| `/auth` | GET | Login / Register page |
| `/userlog` | POST | User login |
| `/userreg` | POST | User registration |
| `/logged` | GET | Dashboard with live sensor charts |
| `/aqi` | GET | AQI prediction input form |
| `/predict` | POST | Run prediction and generate route map |
| `/analytics` | GET | Full analytics dashboard |
| `/graphs` | GET | Model training graphs |
| `/api/sensor-data` | GET | JSON — current sensor readings |
| `/api/sensor-history` | GET | JSON — last 20 historical readings |
| `/logout` | GET | Logout and redirect to home |

---

## Screenshots

> Add screenshots of the dashboard, prediction results, and route map here.

---

## Authors

- **Pradeep S S** — TOCE, Bangalore

---

## License

This project is for academic and educational purposes.
