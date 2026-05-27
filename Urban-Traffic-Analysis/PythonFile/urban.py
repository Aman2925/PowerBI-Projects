# =========================================================
# URBAN TRAFFIC & MOBILITY DATASET GENERATOR
# =========================================================
# Generates realistic messy real-world datasets for:
# 1. Trips Table
# 2. Weather Table
# 3. Traffic Sensor Table
#
# Output:
# - trips_data.csv
# - weather_data.csv
# - traffic_sensor_data.csv
#
# Dataset Size:
# ~300,000+ trip rows
#
# Features:
# ✅ Missing values
# ✅ Duplicate rows
# ✅ Mixed date formats
# ✅ Typos & inconsistent categories
# ✅ Outliers
# ✅ Impossible values
# ✅ Realistic correlations
#
# =========================================================

import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# =========================================================
# CONFIG
# =========================================================

NUM_TRIPS = 300000
NUM_WEATHER = 80000
NUM_SENSORS = 100000

OUTPUT_TRIPS = "trips_data.csv"
OUTPUT_WEATHER = "weather_data.csv"
OUTPUT_SENSORS = "traffic_sensor_data.csv"

# =========================================================
# MASTER DATA
# =========================================================

cities = [
    "Mumbai", "mumbai", "MUMBAI", "Bombay", "Mubmai",
    "Delhi", "delhi", "DELHI",
    "Pune", "PUNE", "pune",
    "Bangalore", "bengaluru", "Banglore",
    "Hyderabad", "HYD", "Hyderbad"
]

vehicle_types = [
    "Car", "Bike", "Auto", "EV", "SUV",
    "car", "AUTO", "Electric"
]

ride_statuses = [
    "Completed", "complete", "Completed ",
    "done", "Cancelled", "cancelled",
    "CANCELLED"
]

traffic_levels = [
    "Low", "Medium", "High",
    "low", "HIGH"
]

weather_conditions = [
    "Clear", "Rain", "Fog",
    "Cloudy", "Storm", None
]

payment_modes = [
    "UPI", "Cash", "Card",
    "upi", "cash ", "Debit Card"
]

sensor_statuses = [
    "Active", "Inactive",
    "active", "inactive"
]

junctions = [
    "Andheri Signal",
    "Bandra Junction",
    "Dadar Circle",
    "Powai Lake Road",
    "Cyber Hub",
    "MG Road",
    "Airport Junction"
]

# =========================================================
# RANDOM DATE GENERATOR
# =========================================================

def random_datetime():
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2026, 5, 1)

    delta = end_date - start_date
    random_days = random.randint(0, delta.days)

    random_seconds = random.randint(0, 86400)

    return start_date + timedelta(
        days=random_days,
        seconds=random_seconds
    )

# =========================================================
# MIXED DATE FORMATS
# =========================================================

def mixed_date_format(dt):

    formats = [
        dt.strftime("%Y-%m-%d %H:%M:%S"),
        dt.strftime("%d/%m/%Y %H:%M"),
        dt.strftime("%b %d %Y %I:%M %p"),
        dt.strftime("%m-%d-%Y %H:%M")
    ]

    return random.choice(formats)

# =========================================================
# GENERATE TRIPS TABLE
# =========================================================

print("Generating Trips Table...")

trip_rows = []

for i in range(NUM_TRIPS):

    start_time = random_datetime()

    duration = abs(np.random.normal(45, 20))

    # Intentional impossible values
    if random.random() < 0.002:
        duration = -10

    end_time = start_time + timedelta(minutes=max(duration, 1))

    distance = abs(np.random.normal(12, 6))

    if random.random() < 0.002:
        distance = 0

    speed = distance / (duration / 60) if duration > 0 else 0

    # Impossible speeds
    if random.random() < 0.002:
        speed = 350

    fuel = round(distance * np.random.uniform(0.05, 0.15), 2)

    # Outlier fuel values
    if random.random() < 0.001:
        fuel = 100

    rating = random.randint(1, 5)

    # Invalid ratings
    if random.random() < 0.001:
        rating = 7

    row = {
        "trip_id": f"T{i+1}",
        "vehicle_id": f"V{random.randint(1000,9999)}",
        "driver_id": f"D{random.randint(100,999)}",
        "city": random.choice(cities),
        "start_time": mixed_date_format(start_time),
        "end_time": mixed_date_format(end_time),
        "pickup_lat": round(np.random.uniform(18.8, 19.3), 6),
        "pickup_long": round(np.random.uniform(72.7, 73.0), 6),
        "drop_lat": round(np.random.uniform(18.8, 19.3), 6),
        "drop_long": round(np.random.uniform(72.7, 73.0), 6),
        "distance_km": round(distance, 2),
        "duration_min": round(duration, 2),
        "avg_speed": round(speed, 2),
        "fuel_consumed": fuel,
        "traffic_level": random.choice(traffic_levels),
        "ride_status": random.choice(ride_statuses),
        "vehicle_type": random.choice(vehicle_types),
        "weather_condition": random.choice(weather_conditions),
        "surge_multiplier": round(np.random.uniform(1, 3), 2),
        "toll_cost": round(np.random.uniform(-50, 500), 2),
        "payment_mode": random.choice(payment_modes),
        "customer_rating": rating,
        "sensor_status": random.choice(sensor_statuses)
    }

    # =====================================================
    # RANDOM NULLS
    # =====================================================

    for col in [
        "customer_rating",
        "fuel_consumed",
        "weather_condition",
        "pickup_lat"
    ]:
        if random.random() < 0.08:
            row[col] = None

    trip_rows.append(row)

# =========================================================
# DUPLICATE ROWS
# =========================================================

duplicates = random.sample(trip_rows, 6000)
trip_rows.extend(duplicates)

trips_df = pd.DataFrame(trip_rows)

# Shuffle dataset
trips_df = trips_df.sample(frac=1).reset_index(drop=True)

trips_df.to_csv(OUTPUT_TRIPS, index=False)

print(f"Trips Dataset Saved: {OUTPUT_TRIPS}")

# =========================================================
# WEATHER TABLE
# =========================================================

print("Generating Weather Table...")

weather_rows = []

for i in range(NUM_WEATHER):

    dt = random_datetime()

    row = {
        "weather_id": f"W{i+1}",
        "city": random.choice(cities),
        "datetime": mixed_date_format(dt),
        "temperature": round(np.random.uniform(18, 42), 1),
        "rainfall_mm": round(np.random.uniform(0, 150), 2),
        "humidity": round(np.random.uniform(40, 100), 1),
        "visibility_km": round(np.random.uniform(0.5, 15), 1),
        "wind_speed": round(np.random.uniform(1, 45), 1),
        "weather_type": random.choice(weather_conditions)
    }

    # Missing values
    if random.random() < 0.07:
        row["visibility_km"] = None

    weather_rows.append(row)

weather_df = pd.DataFrame(weather_rows)

weather_df.to_csv(OUTPUT_WEATHER, index=False)

print(f"Weather Dataset Saved: {OUTPUT_WEATHER}")

# =========================================================
# TRAFFIC SENSOR TABLE
# =========================================================

print("Generating Traffic Sensor Table...")

sensor_rows = []

for i in range(NUM_SENSORS):

    row = {
        "sensor_id": f"S{i+1}",
        "junction_name": random.choice(junctions),
        "congestion_level": random.choice(traffic_levels),
        "avg_wait_time": round(np.random.uniform(5, 120), 1),
        "signal_cycles": random.randint(1, 20),
        "accident_reported": random.choice(["Yes", "No"]),
        "roadwork_flag": random.choice(["Yes", "No"])
    }

    # Outliers
    if random.random() < 0.001:
        row["avg_wait_time"] = 500

    sensor_rows.append(row)

sensor_df = pd.DataFrame(sensor_rows)

sensor_df.to_csv(OUTPUT_SENSORS, index=False)

print(f"Sensor Dataset Saved: {OUTPUT_SENSORS}")

# =========================================================
# SUMMARY
# =========================================================

print("\n===================================")
print("ALL DATASETS GENERATED SUCCESSFULLY")
print("===================================")

print(f"Trips Rows: {len(trips_df)}")
print(f"Weather Rows: {len(weather_df)}")
print(f"Sensor Rows: {len(sensor_df)}")
print("\nFiles Ready For Dashboard Project 🚀")