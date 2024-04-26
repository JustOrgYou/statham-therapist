FROM python:3.11

RUN pip install poetry

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry install

COPY ./app ./app

ENTRYPOINT [ "poetry", "run", "uvicorn", "--host=0.0.0.0", "app.main:app" ]
