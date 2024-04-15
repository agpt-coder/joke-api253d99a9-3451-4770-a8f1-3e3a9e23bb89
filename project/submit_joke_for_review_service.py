from typing import Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class SubmitJokeForReviewResponse(BaseModel):
    """
    The response after a joke is submitted for moderation. Includes whether the submission was successful and any relevant messages.
    """

    success: bool
    message: str
    jokeId: Optional[str] = None


async def submit_joke_for_review(
    setup: str, punchline: str, submitterId: str, language: Optional[str] = None
) -> SubmitJokeForReviewResponse:
    """
    Submits a new joke to the moderation queue.

    Args:
    setup (str): The setup part of the joke.
    punchline (str): The punchline of the joke.
    submitterId (str): The unique identifier for the user submitting the joke.
    language (Optional[str]): The language in which the joke is written. Defaults to 'en' if not provided.

    Returns:
    SubmitJokeForReviewResponse: The response after a joke is submitted for moderation. Includes whether the submission was successful and any relevant messages.
    """
    if not language:
        language = "en"
    try:
        joke = await prisma.models.Joke.prisma().create(
            data={
                "setup": setup,
                "punchline": punchline,
                "language": language,
                "createdByUserId": submitterId,
                "moderationQueues": {
                    "create": {"status": prisma.enums.ModerationStatus.PENDING}
                },
            }
        )
        return SubmitJokeForReviewResponse(
            success=True,
            message="Joke submitted for review successfully.",
            jokeId=joke.id,
        )
    except Exception as e:
        return SubmitJokeForReviewResponse(
            success=False, message=f"Failed to submit joke for review. Error: {str(e)}"
        )
