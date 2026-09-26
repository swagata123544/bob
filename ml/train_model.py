import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# Load dataset
df = pd.read_csv("data/queue_data.csv")

print("Dataset loaded!")
print("Total records:", len(df))


# Features used by BOB
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

X = df[features]
y = df["queue_30min"]


# Time-based train/test split
split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]


print("Training records:", len(X_train))
print("Testing records:", len(X_test))


# Create Random Forest model
print()
print("Training Random Forest model...")

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=12,
    random_state=42,
    n_jobs=-1
)


# Train model
model.fit(X_train, y_train)

print("Training complete!")


# Make predictions
predictions = model.predict(X_test)


# Calculate metrics
mae = mean_absolute_error(y_test, predictions)

mse = mean_squared_error(y_test, predictions)

rmse = mse ** 0.5

r2 = r2_score(y_test, predictions)


# Display results
print()
print("==============================")
print("         BOB ML RESULTS")
print("==============================")

print("MAE :", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R²  :", round(r2, 3))


# Feature importance
importance = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
})

importance = importance.sort_values(
    "importance",
    ascending=False
)


print()
print("==============================")
print("       FEATURE IMPORTANCE")
print("==============================")

print(importance.to_string(index=False))


# Save trained model
joblib.dump(
    model,
    "models/bob_queue_model.pkl"
)

print()
print("Model saved successfully!")
print("Location: models/bob_queue_model.pkl")