"""
Helper functions to process JSON data
"""

import json

from celebi.core.exceptions import QuestionValueError


def remove_backticked_lines(input_str):
    """
    Written by ChatGPT
    """
    lines = input_str.splitlines()

    # Check if the first line starts with a backtick and remove it
    if lines and lines[0].startswith("`"):
        lines.pop(0)

    # Check if the last line starts with a backtick and remove it
    if lines and lines[-1].startswith("`"):
        lines.pop(-1)

    # Join the remaining lines back into a single string
    return "\n".join(lines)


def validate_json_structure(parsed_json):
    """
    Written by ChatGPT
    """
    if not isinstance(parsed_json, dict):
        raise QuestionValueError("Parsed data is not a valid JSON object.")

    required_fields = ["question_text", "responses"]

    # Check for the presence of required fields
    for field in required_fields:
        if field not in parsed_json:
            raise QuestionValueError(f"Missing required field: {field}")

    # Validate responses field
    if not isinstance(parsed_json["responses"], list):
        raise QuestionValueError("The 'responses' field must be a list.")

    for response in parsed_json["responses"]:
        if not isinstance(response, dict):
            raise QuestionValueError("Each item in 'responses' must be an object.")
        if "response_text" not in response:
            raise QuestionValueError("Each response must have 'response_text'.")
        if "scores" not in response:
            raise QuestionValueError("Each response must have 'scores'.")
        if not isinstance(response["scores"], list) or len(response["scores"]) != 6:
            raise QuestionValueError("The 'scores' field must be a list of 6 integers.")

    return True


def jsonify_prompt(prompt_raw: str):
    """
    This function (1) removes code ticks, (2) parses into a JSON object, and (3) makes sure all fields exist.

    Written by ChatGPT
    """
    cleaned_input = remove_backticked_lines(prompt_raw)

    try:
        parsed_json = json.loads(cleaned_input)
    except json.JSONDecodeError as e:
        raise QuestionValueError("Input string is not a valid JSON format.") from e

    if validate_json_structure(parsed_json):
        return parsed_json
