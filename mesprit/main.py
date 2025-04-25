from mesprit.engine import PapalLLMEngine
from mesprit.consensus import consensus, qualitative_consensus, quantitative_consensus

import pandas as pd
import time

pope_list = pd.read_csv("popes.csv")
engine = PapalLLMEngine("gpt-4o")


def generate_prompts(name, url):
    the_pope = f"Pope {name} ({url})"

    prompt_chinese_zodiac = (
        f"What was the Chinese Zodiac sign of {the_pope}? Return only the name of the animal. Do not explain."
    )
    prompt_birthdate = f"What was the birthdate in mm/dd/yyyy format of {the_pope}? Reference the Wikipedia page. If history does not know, write N/A. Do not explain."
    prompt_deathdate = f"What was the deathdate in mm/dd/yyyy format of {the_pope}? Reference the Wikipedia page. If history does not know, write N/A. Do not explain."
    prompt_papacy_start_date = f"What was the papacy start date, i.e. NOT death date, in mm/dd/yyyy format of {the_pope}? Reference the Wikipedia page. Do not explain. Only answer with the date."
    prompt_western_zodiac = f"What was the Western zodiac star sign of {the_pope}? Reference the Wikipedia page. Do not explain. Just provide a one word answer."
    prompt_conservative = f"On a scale of 0 to 10000, how conservative was {the_pope}? Reference the Wikipedia page. Report only the number. Do not explain."

    return [
        (prompt_chinese_zodiac, "A", "chinese_zodiac"),
        (prompt_birthdate, "A", "birthdate"),
        (prompt_deathdate, "A", "deathdate"),
        (prompt_papacy_start_date, "A", "papacy_start_date"),
        (prompt_western_zodiac, "A", "western_zodiac"),
        (prompt_conservative, "1", "conservativeness"),
    ]


blank_prompts = generate_prompts("banana", "apple")
column_names = ["name", "url"]
for p in blank_prompts:
    if p[1] == "1":
        column_names.append(p[2] + "_mean")
        column_names.append(p[2] + "_sd")
        column_names.append(p[2] + "_sample_size")
    else:  # p[1] == "A"
        column_names.append(p[2])

all_papal_rows = []
# for pope in pope_list.iloc:
#     name = pope.pope_name
#     print(f"Got to pope {name}")

#     url = pope.wikipedia_article_link
#     papal_row = [name, url]

#     llm_prompts = generate_prompts(name, url)
#     for prompt in llm_prompts:
#         prompt_msg, aggregator, column_name = prompt
#         print(f"\tDoing prompt {column_name}")

#         consensus_results = consensus(engine, prompt_msg)

#         if aggregator == "1":
#             mean, sd, sample_size = quantitative_consensus(consensus_results)
#             papal_row.append(mean)
#             papal_row.append(sd)
#             papal_row.append(sample_size)
#         else:  # "A"
#             agreed_value = qualitative_consensus(engine, consensus_results, prompt_msg)
#             papal_row.append(agreed_value)

#     print(f"Got row {papal_row}. Sleeping for 10 seconds before next pope...")
#     time.sleep(10)
#     all_papal_rows.append(papal_row)

dataframe = pd.DataFrame(all_papal_rows, columns=column_names)
dataframe.to_csv("popes_data.csv")
