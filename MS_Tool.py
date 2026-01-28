import os, requests, json, time
CHARACTER_ID = "2012,30538,21601,1053429,1103213,1012543,1022237"
ACTIONS = ["stand1", "walk1", "alert", "swingO1", "swingO2", "swingO3", "jump"]
def run():
    save_path = "MS_Export"
    os.makedirs(save_path, exist_ok=True)
    for action in ACTIONS:
        print(f"Downloading {action}...")
        action_dir = os.path.join(save_path, action)
        os.makedirs(action_dir, exist_ok=True)
        with open(os.path.join(action_dir, f"{action}.json"), 'w') as f:
            json.dump({"action": action, "frames": [{"frame": i, "x": -26, "y": -65} for i in range(4)]}, f)
        for frame in range(4):
            r = requests.get(f"https://maplestory.io/api/character/{CHARACTER_ID}/{action}/{frame}")
            if r.status_code == 200:
                with open(os.path.join(action_dir, f"{action}_{frame}.png"), 'wb') as f:
                    f.write(r.content)
            else: break
    print("Done!")

if __name__ == "__main__":
    run()