import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class ReviewJokeResponse(BaseModel):
    """
    Confirms the review action taken on a joke submission.
    """

    success: bool
    message: str
    jokeId: str
    decision: str


async def review_joke(jokeId: str, decision: str) -> ReviewJokeResponse:
    """
    Review and approve or reject a joke submission.

    Args:
        jokeId (str): The unique identifier of the joke being reviewed.
        decision (str): The moderator's decision on the joke submission. Possible values: 'APPROVED', 'REJECTED'.

    Returns:
        ReviewJokeResponse: Confirms the review action taken on a joke submission.
    """
    if decision.upper() not in ["APPROVED", "REJECTED"]:
        return ReviewJokeResponse(
            success=False,
            message="Invalid decision. Choices are 'APPROVED' or 'REJECTED'.",
            jokeId=jokeId,
            decision=decision,
        )
    joke = await prisma.models.Joke.prisma().find_unique(where={"id": jokeId})
    if joke is None:
        return ReviewJokeResponse(
            success=False,
            message=f"Joke with ID {jokeId} not found.",
            jokeId=jokeId,
            decision=decision,
        )
    update_data = {"approved": True if decision == "APPROVED" else False}
    await prisma.models.Joke.prisma().update(where={"id": jokeId}, data=update_data)
    mod_status = (
        prisma.enums.ModerationStatus.APPROVED
        if decision == "APPROVED"
        else prisma.enums.ModerationStatus.REJECTED
    )
    await prisma.models.ModerationQueue.prisma().update_many(
        where={"jokeId": jokeId}, data={"status": mod_status}
    )
    return ReviewJokeResponse(
        success=True,
        message=f"Joke {jokeId} has been {decision.lower()}.",
        jokeId=jokeId,
        decision=decision,
    )
