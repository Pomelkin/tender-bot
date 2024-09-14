import logging
from datetime import datetime

from generation.src.generator.clients import client_author, client_editor
from generation.src.generator.html import get_html
from generation.src.generator.prompts import (
    author_prompt,
    author_system_prompt,
    editor_prompt,
    entity_extractor_prompt,
)


def author_generate(system_message, user_message, max_tokens=1024) -> str:
    completion = client_author.chat.completions.create(
        model="Qwen/Qwen2-7B-Instruct",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        max_tokens=max_tokens,
        temperature=0.0,
    )

    return completion.choices[0].message.content


def editor_generate(user_message, max_tokens=1024) -> str:
    completion = client_editor.chat.completions.create(
        model="google/gemma-2-9b-it",
        messages=[{"role": "user", "content": user_message}],
        max_tokens=max_tokens,
        temperature=0.0,
    )

    return completion.choices[0].message.content


def generate(text, query) -> str:
    author_generation = author_generate(
        system_message=author_system_prompt,
        user_message=author_prompt.format(query, text),
    )

    editor_generation = editor_generate(
        user_message=editor_prompt.format(query, author_generation)
    )

    entities_str = author_generate(
        user_message=entity_extractor_prompt.format(text[:2000] + text[-500:])
    )

    entities = entities_str.split("\n")

    try:
        entities = entities_str.split("\n")
        number = entities[0]
        place = entities[1]
        party_1 = entities[2]
        name_1 = entities[3]
        position_1 = entities[4]
        party_2 = entities[5]
        name_2 = entities[6]
        position_2 = entities[7]
    except Exception as e:
        logging.error(e)
        number = "-"
        place = "-"
        party_1 = "-"
        name_1 = "-"
        position_1 = "-"
        party_2 = "-"
        name_2 = "-"
        position_2 = "-"

    date = datetime.now().strftime("%d.%m.%y")

    html_str = get_html(
        date=date,
        number=number,
        place=place,
        party_1=party_1,
        name_1=name_1,
        position_1=position_1,
        party_2=party_2,
        name_2=name_2,
        position_2=position_2,
        editor_generation=editor_generation,
    )

    return html_str
