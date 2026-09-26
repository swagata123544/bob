import pandas as pd
import joblib


# ==========================================
# LOAD BOB MODEL
# ==========================================

model = joblib.load(
    "models/bob_queue_model.pkl"
)


# ==========================================
# FUNCTION TO UPDATE DERIVED FEATURES
# ==========================================

def prepare_conditions(conditions):

    conditions["processing_capacity"] = (
        conditions["staff_count"]
        * 60
        / conditions["processing_time"]
    )

    conditions["queue_pressure"] = (
        conditions["arrival_rate"]
        / conditions["processing_capacity"]
    )

    return conditions


# ==========================================
# CURRENT CONDITIONS
# ==========================================

base_conditions = {

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
}


# ==========================================
# PREDICTION FUNCTION
# ==========================================

def predict_scenario(conditions):

    conditions = prepare_conditions(
        conditions.copy()
    )

    # IMPORTANT:
    # Keep exactly the same feature order
    # that was used during model training.

    features = [
        "current_queue",
        "arrival_rate",
        "processing_time",
        "processing_capacity",
        "queue_pressure",
        "staff_count",
        "complexity",
        "hour",
        "day_of_week",
        "system_delay",
        "staff_shortage",
        "demand_spike"
    ]

    data = pd.DataFrame(
        [conditions],
        columns=features
    )

    prediction = model.predict(data)[0]

    return round(prediction)


# ==========================================
# SCENARIO 1
# ==========================================

do_nothing = base_conditions.copy()


# ==========================================
# SCENARIO 2
# ADD ONE OFFICER
# ==========================================

add_officer = base_conditions.copy()

add_officer["staff_count"] = 3

add_officer["staff_shortage"] = 0


# ==========================================
# SCENARIO 3
# IMPROVE PROCESSING
# ==========================================

faster_processing = base_conditions.copy()

faster_processing["processing_time"] = 8


# ==========================================
# SCENARIO 4
# REDUCE ARRIVALS
# ==========================================

reduce_arrivals = base_conditions.copy()

reduce_arrivals["arrival_rate"] = 22


# ==========================================
# RUN SIMULATIONS
# ==========================================

results = {

    "Do nothing":
        predict_scenario(do_nothing),

    "Add 1 officer":
        predict_scenario(add_officer),

    "Improve processing":
        predict_scenario(faster_processing),

    "Reduce arrivals":
        predict_scenario(reduce_arrivals)

}


# ==========================================
# DISPLAY
# ==========================================

print()
print("========================================")
print("        BOB WHAT-IF SIMULATOR")
print("========================================")

print()

print(
    "Current queue:",
    base_conditions["current_queue"]
)

print()

for scenario, prediction in results.items():

    print(
        f"{scenario:<25} -> {prediction} people"
    )


# ==========================================
# COMPARE WITH CURRENT QUEUE
# ==========================================

print()

print("----------------------------------------")

for scenario, prediction in results.items():

    change = prediction - base_conditions["current_queue"]

    if change > 0:

        print(
            f"{scenario:<25} : +{change} people"
        )

    elif change < 0:

        print(
            f"{scenario:<25} : {change} people"
        )

    else:

        print(
            f"{scenario:<25} : no change"
        )


# ==========================================
# FIND LOWEST PREDICTED QUEUE
# ==========================================

best_scenario = min(
    results,
    key=results.get
)

best_prediction = results[
    best_scenario
]


print()
print("========================================")

print(
    "Lowest predicted queue:",
    best_prediction
)

print(
    "Intervention scenario:",
    best_scenario
)

print("========================================")