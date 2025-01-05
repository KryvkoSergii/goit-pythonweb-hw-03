FROM python:3.13-slim
ENV APP_HOME=/app
WORKDIR $APP_HOME
COPY . .
RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
EXPOSE 3000
ENTRYPOINT ["poetry", "run", "python", "./app/main.py"]