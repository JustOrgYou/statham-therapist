FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y locales

RUN echo "LC_ALL=en_US.UTF-8" >> /etc/environment
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
RUN echo "LANG=en_US.UTF-8" > /etc/locale.conf
RUN locale-gen en_US.UTF-8

RUN pip install poetry

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry install

COPY . .

ENTRYPOINT [ "poetry", "run", "streamlit", "run", "💬_Chat.py", "--server.address=0.0.0.0" ]

# ENTRYPOINT tail -f /dev/null
