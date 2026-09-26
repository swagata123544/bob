import pandas as pd
import joblib


# Load BOB's trained model
model = joblib.load(
    "models/bob_queue_model.pkl"
)


# --------------------------------
# CURRENT LIVE SITUATION
# --------------------------------

live_data = pd.DataFrame([{

    "current_queue": 42,

    "arrival_rate": 32,

    "processing_time": 11,

    "staff_count": 2,

    "complexity": 0.75,

    "hour": 10,

    "day_of_week": 0,

    "system_delay": 0,

    "staff_shortage": 1,

    "demand_spike": 0

}])


# --------------------------------
# PREDICT
# --------------------------------

prediction = model.predict(
    live_data
)[0]


current_queue = live_data.iloc[0]["current_queue"]


print()
print("==============================")
print("       BOB QUEUE FORECAST")
print("==============================")

print(
    "Current queue:",
    current_queue
)

print(
    "Predicted queue in 30 minutes:",
    round(prediction)
)


# --------------------------------
# CONGESTION LEVEL
# --------------------------------

print()

if prediction >= 60:

    print("STATUS: HIGH CONGESTION RISK")

elif prediction >= 45:

    print("STATUS: MODERATE CONGESTION RISK")

else:

    print("STATUS: LOW CONGESTION RISK")


# --------------------------------
# QUEUE CHANGE
# --------------------------------

change = prediction - current_queue

print()

if change > 0:

    print(
        "Expected queue increase:",
        round(change),
        "people"
    )

elif change < 0:

    print(
        "Expected queue decrease:",
        round(abs(change)),
        "people"
    )

else:

    print("Expected queue change: 0 people")