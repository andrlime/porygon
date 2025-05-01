from mesprit.engine import PapalLLMEngine
from mesprit.consensus import consensus, qualitative_consensus, quantitative_consensus

from concurrent.futures import ThreadPoolExecutor, as_completed
from io import StringIO
import os
import pandas as pd
import time
from collections import defaultdict

pope_list = pd.read_csv("popes.csv")
sys_prompt = """
You are a helpful bot that simulates hunger games between 24 historical popes. We care about the following metrics:
1. Kills per character (an integer number)
2. Heroic events (e.g. saving other people) per character (an integer number)
3. Deaths per character (an integer number)
4. Whether that character won (either 1 or 0)

Please respond in CSV format with the following header:
character_name,kills,heroic_events,deaths,win

If the character name contains a comma, DO NOT UNDER ANY CIRCUMSTANCES INCLUDE THE COMMA OR YOU WILL BE EXCOMMUNICATED.

Do not respond with code ticks. Please reply with the raw CSV.

Finally, after the raw CSV, please add a newline with the following string "THIS IS WHERE THE DATA ENDS" and then another newline.

Afterwards, please append some highlights from the game (e.g. X killed Y, X found fruit in a basket, X jumped off a cliff, etc) consistent with the CSV data.

The user will provide you with a list of pope names. Use what you know about the popes, e.g. their strength, their political beliefs, etc.
"""
sys_prompt = """
You are a helpful political scientist. The user will provide a Pope name. Using what you know about the pope, gauge how conservative they are on a scale of 1 to 1000000. DO NOT return anything except the final number. NO code ticks, NO weird formatting, NO refusals, JUST RAW DIGITS. Otherwise, YOU WILL BE EXCOMMUNICATED.

Access the given wikipedia URL for more information.
"""
engine = PapalLLMEngine("gpt-4.1-nano", sys_prompt)

sample_size = 24
iterations = 3

def aggregate_pope_results(folder_path):
    stats = defaultdict(lambda: {"kills": 0, "heroic_events": 0, "deaths": 0, "win": 0, "games": 0})

    for filename in os.listdir(folder_path):
        print(filename)
        if not filename.endswith(".log"):
            continue

        with open(os.path.join(folder_path, filename), "r") as f:
            content = f.read()

        if "THIS IS WHERE THE DATA ENDS" not in content:
            continue

        csv_data = content.split("THIS IS WHERE THE DATA ENDS")[0].strip()

        df = pd.read_csv(StringIO(csv_data.strip()))
        
        for _, row in df.iterrows():
            pope = row['character_name']
            stats[pope]["kills"] += row['kills']
            stats[pope]["heroic_events"] += row['heroic_events']
            stats[pope]["deaths"] += row['deaths']
            stats[pope]["win"] += row['win']
            stats[pope]["games"] += 1

    # Convert to DataFrame for easier viewing/export
    final_df = pd.DataFrame([
        {
            "character_name": pope,
            "total_kills": data["kills"],
            "total_heroic_events": data["heroic_events"],
            "total_deaths": data["deaths"],
            "total_wins": data["win"],
            "games_played": data["games"],
            "kill_death_ratio": round(data["kills"] / data["deaths"], 2) if data["deaths"] else float("inf"),
            "heroic_death_ratio": round(data["heroic_events"] / data["deaths"], 2) if data["deaths"] else float("inf"),
            "win_percentage": round(100 * data["win"] / data["games"], 2) if data["games"] else 0
        }
        for pope, data in stats.items()
    ])

    final_df.to_csv("popes_hunger_games_data.csv")

columns = ["pope_name", "conservativeness_mean", "conservativeness_sd"]
all_rows = []
def thread_worker(pope):
    name = pope.pope_name
    print(f"pope {name}")

    if os.path.isfile(f"./data/cons/{name}.csv"):
        with open(f"./data/cons/{name}.csv", "r") as f:
            d = f.read().split("\n")[1].split(",")
            mean, sd, sample_size = d[0], d[1], d[2]
            return [name, mean, sd]
    
    url = pope.pope_url
    papal_row = [name, url]

    results = consensus(engine, f"{name} ({url})")
    mean, sd, sample_size = quantitative_consensus(results)

    with open(f"./data/cons/{name}.csv", "w") as f:
        f.write(f"mean,sd,n\n{mean},{sd},{sample_size}\n")

    return [mean, name, sd]

with ThreadPoolExecutor(max_workers=32) as executor:
    futures = [executor.submit(thread_worker, pope) for pope in pope_list.iloc]
    for future in as_completed(futures):
        all_rows.append(future.result())

dataframe = pd.DataFrame(all_rows, columns=columns)
dataframe.to_csv("popes_data.csv")

# aggregate_pope_results("./data")
