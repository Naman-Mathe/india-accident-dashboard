import pandas as pd
import numpy as np

# States in India
states = [
    "Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "Uttar Pradesh",
    "Gujarat", "Rajasthan", "West Bengal", "Punjab", "Haryana",
    "Bihar", "Madhya Pradesh", "Kerala", "Odisha", "Assam"
]

causes = ["Speeding", "Drunk Driving", "Overtaking", "Weather", "Vehicle Defect"]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

data = []

# Generate 15,000 rows
for _ in range(15000):
    year = np.random.randint(2015, 2024)
    state = np.random.choice(states)
    accidents = np.random.randint(100, 5000)
    fatalities = int(accidents * np.random.uniform(0.1, 0.3))
    cause = np.random.choice(causes)
    month = np.random.choice(months)

    data.append([year, state, accidents, fatalities, cause, month])

df = pd.DataFrame(data, columns=[
    "Year", "State", "Accidents", "Fatalities", "Cause", "Month"
])

# Save file
df.to_csv("data/accidents.csv", index=False)
print("Dataset created successfully!")