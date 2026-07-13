FROM python:3.12-slim

ARG UID=1000
ARG GID=1000

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN groupadd -g $GID appuser && useradd -u $UID -g $GID -m appuser

COPY ./app /code/app

USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]