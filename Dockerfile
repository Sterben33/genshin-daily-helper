FROM docker.io/oz123/pipenv:3.11-v2023-6-26 AS builder


ENV PIPENV_VENV_IN_PROJECT=1

ADD Pipfile.lock Pipfile /usr/src/

WORKDIR /usr/src

RUN /root/.local/bin/pipenv sync

RUN /usr/src/.venv/bin/python -c "import requests; print(requests.__version__)"

FROM docker.io/python:3.11 AS runtime

RUN mkdir -v /usr/src/.venv

COPY --from=builder /usr/src/.venv/ /usr/src/.venv/

RUN /usr/src/.venv/bin/python -c "import requests; print(requests.__version__)"

WORKDIR /usr/src/

RUN pipenv install
COPY . .

USER coolio

CMD ["./.venv/bin/python", "-m", "main.py"]