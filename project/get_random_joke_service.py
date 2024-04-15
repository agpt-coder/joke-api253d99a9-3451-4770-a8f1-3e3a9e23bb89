import random

import prisma
import prisma.models
from fastapi import HTTPException
from pydantic import BaseModel


class RandomJokeResponse(BaseModel):
    """
    Response model containing the random knock-knock joke fetched from the database.
    """

    setup: str
    punchline: str
    language: str


async def get_random_joke(language: str) -> RandomJokeResponse:
    """
    Fetches a random knock-knock joke.

    This function queries the database for a list of jokes that match the specified
    language. If no jokes are found for the given language, the function raises an HTTP exception.

    Args:
    language (str): The preferred language for the joke. Defaults to 'en' if not specified.

    Returns:
    RandomJokeResponse: Response model containing the random knock-knock joke fetched from the database.

    Example:
    get_random_joke('en')
    > RandomJokeResponse(setup="Knock knock.", punchline="Who's there?", language='en')
    """
    jokes = await prisma.models.Joke.prisma().find_many(
        where={"language": language, "approved": True}
    )
    if not jokes:
        raise HTTPException(
            status_code=404, detail="No jokes found for the specified language."
        )
    joke = random.choice(jokes)
    return RandomJokeResponse(
        setup=joke.setup, punchline=joke.punchline, language=joke.language
    )
