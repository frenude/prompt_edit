import random
import re

from src.client import add_and_run


def get_data():
    text = f"Give me {random.randint(6, 14)} lines of dialogue."
    thread_messages = add_and_run(text, "asst_hBzEVeRj4SvWTiRzzZpIRC6B")
    data = thread_messages.data[0].content[0].text.value
    match = re.search(r'{.*}', data, re.DOTALL)
    if match:
        json_data = match.group(0)
        return json_data
