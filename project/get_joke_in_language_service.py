import random

import prisma
import prisma.models
from pydantic import BaseModel


class JokeResponse(BaseModel):
    """
    Outputs a single joke localized in the user's requested language, alongside some basic identfying data about the joke. This model is designed to be flexible to accommodate jokes in any supported language.
    """

    id: str
    setup: str
    punchline: str
    language: str


async def get_joke_in_language(language: str) -> JokeResponse:
    """
    Fetches a random joke in the specified language.

    Args:
    language (str): The preferred language for the joke defined in the path parameter.

    Returns:
    JokeResponse: Outputs a single joke localized in the user's requested language, alongside some basic identifying data about the joke. This model is designed to be flexible to accommodate jokes in any supported language.
    """
    jokes_in_language = await prisma.models.Joke.prisma().find_many(
        where={"language": language, "approved": True}
    )
    if not jokes_in_language:
        raise ValueError("No jokes found in the specified language.")
    random_joke = random.choice(jokes_in_language)
    return JokeResponse(
        id=random_joke.id,
        setup=random_joke.setup,
        punchline=random_joke.punchline,
        language=random_joke.language,
    )
