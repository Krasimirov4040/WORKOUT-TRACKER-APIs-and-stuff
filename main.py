import requests
import os
import json

from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from datetime import datetime
BASE_URL="https://app.100daysofpython.dev"
sheety_endpoint="https://api.sheety.co/e536b57a9e762fb8696aeba6f3353e36/myWorkouts/workouts"
calories_calculate_endpoint=f"{BASE_URL}/v1/nutrition/natural/exercise"
load_dotenv()
API_KEY=os.getenv("API_KEY")
APP_ID=os.getenv("APP_ID")
USER=os.getenv("SHEETY_USER")
PASS=os.getenv("SHEETY_PASS")
print(API_KEY)
print(USER)

basic=HTTPBasicAuth(USER, PASS)
headers={
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}
print(
    """Supported activities:

Running/Jogging - "ran for 30 minutes", "jogged 2 miles"
Swimming - "swam for 1 hour", "swimming laps"
Walking - "walked 3 miles", "brisk walk 45 min"
Cycling - "biked for 1 hour", "rode bike 10 miles"
Weightlifting - "lifted weights 45 min", "weight training"""
      )
print("\n\n\n")
activity=input("Tell me which exercises you did?")
request_parameters={
      "query": activity,
      "weight_kg": 90,
      "height_cm": 187,
      "age": 22,
      "gender": "male"
}
response=requests.post(url=calories_calculate_endpoint, json=request_parameters, headers=headers)
response.raise_for_status()
data=response.json()

# print(json.dumps(data, indent=2))
exercise=str(data["exercises"][0]["name"])
duration_min=data["exercises"][0]["duration_min"]
calories_burned=data["exercises"][0]["nf_calories"]
for exercise in data["exercises"]:
    new_row={
        "workout":{
            "date":datetime.now().strftime("%d/%m/%Y"),
            "time":datetime.now().strftime("%H:%M:%S %p"),
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }

    }
    response = requests.post(sheety_endpoint, json=new_row, auth=basic)  # ← NO headers!
    response.raise_for_status()
