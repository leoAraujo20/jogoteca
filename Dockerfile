FROM python:3.13-slim
ENV POETRY_VIRTUALENVS_CREATE=false 
WORKDIR /app
COPY . .
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi --no-root
EXPOSE 8000
CMD ["python", "run.py"]
