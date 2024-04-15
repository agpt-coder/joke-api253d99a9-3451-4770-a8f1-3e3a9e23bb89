import logging
from contextlib import asynccontextmanager
from typing import Optional

import project.authenticate_user_service
import project.get_api_usage_stats_service
import project.get_joke_in_language_service
import project.get_performance_metrics_service
import project.get_random_joke_service
import project.rate_limit_check_service
import project.review_joke_service
import project.submit_joke_for_review_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="joke-api",
    lifespan=lifespan,
    description="Based on the information gathered, it is understood that the user prefers knock-knock jokes. To fulfill this requirement, it's recommended to develop a single API that returns one knock-knock joke upon request. Given the tech stack specified, here's a succinct plan for this project:\n\n1. **Programming Language**: Utilize Python, a widely used and powerful programming language that is well-suited for web API development.\n\n2. **API Framework**: Implement the API using FastAPI. This modern, fast (high-performance) web framework for building APIs with Python 3.7+ is ideal for quickly creating a joke API thanks to its easy-to-use route declarations that allow for asynchronous handling and its automatic Swagger documentation generation.\n\n3. **Database**: Store the jokes in PostgreSQL. This robust, open-source object-relational database system offers reliability, feature robustness, and performance for storing and retrieving jokes.\n\n4. **ORM (Object-Relational Mapping)**: Utilize Prisma with Python as the ORM to interface with the PostgreSQL database. Prisma's approach to database interaction is developer-friendly and can simplify database operations, such as fetching a random knock-knock joke for the API to serve.\n\nThe API will have a simple endpoint, such as `/joke`, which when accessed will query the database using Prisma to retrieve and return a random knock-knock joke. This design ensures that the API remains scalable, maintainable, and easy to use, both for developers integrating this API into their applications and for end-users looking for a quick laugh.\n\nRemember, this implementation plan is based on preference for knock-knock jokes and utilizes a specified technology stack. The choice of the JokeAPI as a potential source during the research phase suggests exploring existing services; however, creating a custom API offers the advantage of personalized joke selection and the flexibility of future expansions, such as adding categories.",
)


@app.get("/joke", response_model=project.get_random_joke_service.RandomJokeResponse)
async def api_get_get_random_joke(
    language: str,
) -> project.get_random_joke_service.RandomJokeResponse | Response:
    """
    Fetches a random knock-knock joke.
    """
    try:
        res = await project.get_random_joke_service.get_random_joke(language)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/moderation/submit",
    response_model=project.submit_joke_for_review_service.SubmitJokeForReviewResponse,
)
async def api_post_submit_joke_for_review(
    punchline: str, setup: str, submitterId: str, language: Optional[str]
) -> project.submit_joke_for_review_service.SubmitJokeForReviewResponse | Response:
    """
    Submits a new joke to the moderation queue.
    """
    try:
        res = await project.submit_joke_for_review_service.submit_joke_for_review(
            punchline, setup, submitterId, language
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/joke/{language}", response_model=project.get_joke_in_language_service.JokeResponse
)
async def api_get_get_joke_in_language(
    language: str,
) -> project.get_joke_in_language_service.JokeResponse | Response:
    """
    Fetches a random joke in the specified language.
    """
    try:
        res = await project.get_joke_in_language_service.get_joke_in_language(language)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/security/rate_limit",
    response_model=project.rate_limit_check_service.RateLimitCheckResponse,
)
async def api_get_rate_limit_check() -> project.rate_limit_check_service.RateLimitCheckResponse | Response:
    """
    Checks and reports on the current rate limit status of the user.
    """
    try:
        res = await project.rate_limit_check_service.rate_limit_check()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/analytics/usage",
    response_model=project.get_api_usage_stats_service.GetApiUsageStatsResponse,
)
async def api_get_get_api_usage_stats() -> project.get_api_usage_stats_service.GetApiUsageStatsResponse | Response:
    """
    Provides statistics on API usage.
    """
    try:
        res = await project.get_api_usage_stats_service.get_api_usage_stats()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/moderation/review/{jokeId}",
    response_model=project.review_joke_service.ReviewJokeResponse,
)
async def api_put_review_joke(
    jokeId: str, decision: str
) -> project.review_joke_service.ReviewJokeResponse | Response:
    """
    Review and approve or reject a joke submission.
    """
    try:
        res = await project.review_joke_service.review_joke(jokeId, decision)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/auth/login",
    response_model=project.authenticate_user_service.AuthenticationResponse,
)
async def api_post_authenticate_user(
    username_or_email: str, password: str
) -> project.authenticate_user_service.AuthenticationResponse | Response:
    """
    Authenticate users and provide a token for subsequent requests.
    """
    try:
        res = await project.authenticate_user_service.authenticate_user(
            username_or_email, password
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/analytics/performance",
    response_model=project.get_performance_metrics_service.PerformanceMetricsResponse,
)
async def api_get_get_performance_metrics() -> project.get_performance_metrics_service.PerformanceMetricsResponse | Response:
    """
    Provides metrics on API performance.
    """
    try:
        res = await project.get_performance_metrics_service.get_performance_metrics()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
