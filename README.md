---
date: 2024-04-15T18:30:26.522129
author: AutoGPT <info@agpt.co>
---

# joke-api

Based on the information gathered, it is understood that the user prefers knock-knock jokes. To fulfill this requirement, it's recommended to develop a single API that returns one knock-knock joke upon request. Given the tech stack specified, here's a succinct plan for this project:

1. **Programming Language**: Utilize Python, a widely used and powerful programming language that is well-suited for web API development.

2. **API Framework**: Implement the API using FastAPI. This modern, fast (high-performance) web framework for building APIs with Python 3.7+ is ideal for quickly creating a joke API thanks to its easy-to-use route declarations that allow for asynchronous handling and its automatic Swagger documentation generation.

3. **Database**: Store the jokes in PostgreSQL. This robust, open-source object-relational database system offers reliability, feature robustness, and performance for storing and retrieving jokes.

4. **ORM (Object-Relational Mapping)**: Utilize Prisma with Python as the ORM to interface with the PostgreSQL database. Prisma's approach to database interaction is developer-friendly and can simplify database operations, such as fetching a random knock-knock joke for the API to serve.

The API will have a simple endpoint, such as `/joke`, which when accessed will query the database using Prisma to retrieve and return a random knock-knock joke. This design ensures that the API remains scalable, maintainable, and easy to use, both for developers integrating this API into their applications and for end-users looking for a quick laugh.

Remember, this implementation plan is based on preference for knock-knock jokes and utilizes a specified technology stack. The choice of the JokeAPI as a potential source during the research phase suggests exploring existing services; however, creating a custom API offers the advantage of personalized joke selection and the flexibility of future expansions, such as adding categories.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'joke-api'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
