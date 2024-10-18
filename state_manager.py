# state_manager.py - json operations with main and fetching_new_users

import json

STATE_FILE = 'state.json'

def load_state():
    with open(STATE_FILE, 'r') as file:
        state = json.load(file)
        return state

def save_state(state):
    with open(STATE_FILE, 'w') as file:
        try:
            json.dump(state, file, indent=4)
        except Exception as e:
            print(f"Error occurred while saving state: {e}")
