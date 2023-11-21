import json
import re

from src.client import add_and_run


def mark(original, portrait):
    content = json.dumps({
        "original": original,
        "portrait": portrait
    })
    thread_messages = add_and_run(content=content, assistant_id="asst_si7c0wKo1ApNEODG1JrMaunv")
    data = thread_messages.data[0].content[0].text.value.replace('```json\n', '').replace('```', '')
    return json.loads(data)
