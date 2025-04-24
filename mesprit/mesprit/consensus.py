"""
Parallel consensus algorithm for LLMs
TODO: Can add ranked choice voting
"""

from concurrent.futures import ThreadPoolExecutor, as_completed

from collections import Counter
import numpy as np
from uuid import uuid4


def validate(numbers_list):
    validated_list = []
    for n in numbers_list:
        try:
            validated_list.append(int(n))
        except ValueError as _:
            continue
    return validated_list


def quantitative_consensus(values):
    list_of_numbers = validate(values)
    return (float(np.mean(list_of_numbers)), float(np.std(list_of_numbers)), len(list_of_numbers))


def qualitative_consensus(engine, strings, prompt):
    return engine.prompt(
        f"""
Below is a list of answers to a prompt.

{", ".join(strings)}

Please respond with the most common or mode answer after accounting for differences in spelling, plurality, punctuation. Answer in lowercase. Omit any explanation or punctuation.
"""
    )


def seed_prompt(prompt, seed=None):
    if seed is not None:
        return prompt + "\n" + f"seed: {seed}"
    return prompt + "\n" + f"seed: {str(uuid4())}"


def consensus(engine, prompt, N=15):
    results = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(engine.prompt, seed_prompt(prompt)) for _ in range(N)]
        for future in as_completed(futures):
            results.append(future.result())
    return results
