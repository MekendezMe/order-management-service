FROM python:3.13.3

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN pip install --upgrade pip wheel "poetry==1.8.3"
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY src .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

