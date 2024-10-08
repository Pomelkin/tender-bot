import logging
import re
from datetime import datetime

from generation.src.creator.html import get_html
from generation.src.creator.prompts import (
    author_prompt,
    author_system_prompt,
    editor_prompt,
    entity_extractor_prompt,
    verdict_prompt,
)
from generation.src.utils.clients import client_author, client_editor


class Generator:
    async def _author_generate(
        self, system_message, user_message, max_tokens=1024
    ) -> str:
        """
        Generate text using the author model.

        Args:
            system_message (str): The system message to provide to the model.
            user_message (str): The user message to provide to the model.

        Returns:
            str: The generated text.
        """
        completion = await client_author.chat.completions.create(
            model="Qwen/Qwen2-7B-Instruct",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            max_tokens=max_tokens,
            temperature=0.0,
        )
        return completion.choices[0].message.content

    async def _editor_generate(self, user_message, max_tokens=1024) -> str:
        """
        Generate text using the editor model.

        Args:
            user_message (str): The user message to provide to the model.

        Returns:
            str: The generated text.
        """
        completion = await client_editor.chat.completions.create(
            model="google/gemma-2-27b-it",
            messages=[{"role": "user", "content": user_message}],
            max_tokens=max_tokens,
            temperature=0.0,
        )
        return completion.choices[0].message.content

    async def generate_verdict(self, rag_answer) -> bool:
        editor_generation = await self._editor_generate(
            user_message=verdict_prompt.format(rag_answer), max_tokens=2
        )
        logging.info(editor_generation)

        try:
            digits = re.sub("\D", "", editor_generation)
            verdict = bool(int(digits.strip()))
        except Exception as e:
            logging.error(f"{e}: {editor_generation}")
            verdict = False

        logging.info(f"Verdict: {verdict}")
        return verdict

    async def generate(self, text, query) -> str:
        """
        Generate a contract based on the given text and query.

        Args:
            text (str): The text of the contract.
            query (str): The query to generate the contract for.

        Returns:
            str: The generated contract as an HTML string.
        """
        author_generation = await self._author_generate(
            system_message=author_system_prompt,
            user_message=author_prompt.format(query, text),
        )

        editor_generation = await self._editor_generate(
            user_message=editor_prompt.format(query, author_generation)
        )

        entities_str = await self._editor_generate(
            user_message=entity_extractor_prompt.format(text[:2000] + text[-500:])
        )

        entities = entities_str.split("\n")
        
        try:
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

        html_str = await get_html(
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
