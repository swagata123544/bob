import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

rows = []

# Start of simulation
start_date = datetime(2026, 1, 1)

current_date = start_date

working_days_created = 0


# ==========================================
# SIMULATE 90 WORKING DAYS
# ==========================================

while working_days_created < 90:

    # Skip Saturday and Sunday
    if current_date.weekday() >= 5:
        current_date += timedelta(days=1)
        continue

    day_of_week = current_date.weekday()

    # Starting queue for the day
    queue = np.random.randint(5, 15)


    # ======================================
    # SIMULATE 9 AM - 6 PM
    # ======================================

    for minutes in range(0, 9 * 60, 15):

        hour = 9 + minutes // 60
        minute = minutes % 60


        # ==================================
        # TIMESTAMP
        # ==================================

        timestamp = current_date.replace(
            hour=hour,
            minute=minute,
            second=0,
            microsecond=0
        )


        # ==================================
        # ARRIVAL RATE
        # ==================================

        arrival_rate = 18


        # Morning rush
        if 9 <= hour < 11:
            arrival_rate += 12


        # Lunch slowdown
        elif 13 <= hour < 14:
            arrival_rate -= 6


        # Evening slowdown
        elif hour >= 16:
            arrival_rate -= 4


        # Monday rush
        if day_of_week == 0:
            arrival_rate += 7


        # Friday increase
        elif day_of_week == 4:
            arrival_rate += 3


        # Random variation
        arrival_rate += np.random.normal(0, 3)

        arrival_rate = max(2, arrival_rate)


        # ==================================
        # APPLICATION COMPLEXITY
        # ==================================

        complexity = np.random.beta(2, 3)


        # Processing time increases
        # with application complexity
        processing_time = 6 + complexity * 7


        # ==================================
        # SYSTEM DELAY
        # ==================================

        system_delay = 0


        if np.random.random() < 0.05:

            system_delay = np.random.uniform(2, 5)

            processing_time += system_delay


        # ==================================
        # STAFF
        # ==================================

        normal_staff = 3

        staff_count = normal_staff

        staff_shortage = 0


        # 10% probability of staff shortage
        if np.random.random() < 0.10:

            staff_count -= 1

            staff_shortage = 1


        # ==================================
        # DEMAND SPIKE
        # ==================================

        demand_spike = 0


        if np.random.random() < 0.05:

            arrival_rate += np.random.uniform(10, 20)

            demand_spike = 1


        # ==================================
        # PROCESSING CAPACITY
        # ==================================

        processing_capacity = (
            staff_count * 60 / processing_time
        )


        # ==================================
        # QUEUE PRESSURE
        # ==================================

        queue_pressure = (
            arrival_rate / processing_capacity
        )


        # ==================================
        # ARRIVALS AND PROCESSED PEOPLE
        # ==================================

        arrivals = arrival_rate / 4

        processed = processing_capacity / 4


        # Small random operational variation
        noise = np.random.normal(0, 0.8)


        # ==================================
        # NEXT QUEUE
        # ==================================

        next_queue = (
            queue
            + arrivals
            - processed
            + noise
        )


        # Queue cannot be negative
        next_queue = max(0, next_queue)


        # ==================================
        # STORE RECORD
        # ==================================

        rows.append({

            "timestamp": timestamp,

            "day_of_week": day_of_week,

            "hour": hour,

            "minute": minute,

            "current_queue": round(queue),

            "arrival_rate": round(
                arrival_rate,
                2
            ),

            "processing_time": round(
                processing_time,
                2
            ),

            "processing_capacity": round(
                processing_capacity,
                2
            ),

            "queue_pressure": round(
                queue_pressure,
                2
            ),

            "staff_count": staff_count,

            "complexity": round(
                complexity,
                2
            ),

            "system_delay": round(
                system_delay,
                2
            ),

            "staff_shortage": staff_shortage,

            "demand_spike": demand_spike,

            "next_queue": round(
                next_queue
            )

        })


        # Next 15-minute interval
        queue = next_queue


    working_days_created += 1

    current_date += timedelta(days=1)


# ==========================================
# CREATE DATAFRAME
# ==========================================

df = pd.DataFrame(rows)


# ==========================================
# CREATE 30-MINUTE TARGET
# ==========================================

# Two 15-minute intervals = 30 minutes
df["queue_30min"] = (
    df["next_queue"].shift(-2)
)


# Remove rows without a target
df = df.dropna()


df["queue_30min"] = (
    df["queue_30min"].astype(int)
)


# ==========================================
# SAVE DATASET
# ==========================================

df.to_csv(
    "data/queue_data.csv",
    index=False
)


# ==========================================
# DISPLAY INFORMATION
# ==========================================

print()
print("========================================")
print("      BOB DATASET CREATED")
print("========================================")

print()

print(
    "Total records:",
    len(df)
)

print(
    "Average queue:",
    round(
        df["current_queue"].mean(),
        2
    )
)

print(
    "Maximum queue:",
    df["current_queue"].max()
)

print(
    "Demand spikes:",
    df["demand_spike"].sum()
)

print(
    "Staff shortages:",
    df["staff_shortage"].sum()
)

print()

print("Columns:")

print(
    list(df.columns)
)

print()

print("Dataset saved to:")
print("data/queue_data.csv")