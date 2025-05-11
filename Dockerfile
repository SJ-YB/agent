FROM python:3.13 AS builder

WORKDIR /agent

COPY poetry.lock pyproject.toml ./

RUN apt update -y && \
    apt upgrade -y && \
    apt install build-essential -y && \
    pip install poetry==2.1.2 && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction

FROM python:3.13-slim
USER root

ARG PYTHONPATH
ENV PYTHONPATH=$PYTHONPATH:/agent
# https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUNBUFFERED
# https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file
ENV PYTHONBUFFERED=1
# https://docs.python.org/3/using/cmdline.html#envvar-PYTHONDONTWRITEBYTECODE
ENV PYTHONDONTWRITEBYTECODE=1
# https://docs.python.org/3/using/cmdline.html#envvar-PYTHONHASHSEED
ENV PYTHONHASHSEED=0

COPY --from=builder --chown=root:root /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --chown=root:root ./ /agent

WORKDIR /agent
EXPOSE 8000

ENTRYPOINT ["python", "src/main.py", "web", "run"]