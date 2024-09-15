import logging
from datetime import datetime

from generation.src.editor.prompts import prompt
from generation.src.utils.clients import client_editor


class Generator:
    def __init__(self, max_tokens=1024):
        self.max_tokens = max_tokens

    async def _editor_generate(self, user_message) -> str:
        """
        Generate text using the editor model.

        Args:
            user_message (str): The user message to provide to the model.

        Returns:
            str: The generated text.
        """
        completion = await client_editor.chat.completions.create(
            model="google/gemma-2-9b-it",
            messages=[{"role": "user", "content": user_message}],
            max_tokens=self.max_tokens,
            temperature=0.0,
        )
        return completion.choices[0].message.content

    async def generate(self, html, text, query) -> str:
        """
        Generate a portion of a contract based on the given text and query.

        Args:
            html (str): The HTML of the contract.
            text (str): The text of the contract.
            query (str): The query to generate the contract for.

        Returns:
            str: The generated contract as an HTML string.
        """
        editor_generation = await self._editor_generate(
            user_message=prompt.format(html, query, text)
        )

        return editor_generation
