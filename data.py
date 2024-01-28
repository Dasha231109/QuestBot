import json
import os


def load_data_user():
    with open('user_data', 'r') as f:
        return json.load(f)

def save_data_user(user_data):
    with open('user_data', 'w') as f:
        json.dump(user_data, f)


if os.path.exists("user_data.json"):
    user_data = load_data_user()
else:
    user_data = {}
