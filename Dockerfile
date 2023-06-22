FROM python:3.10.9-slim-buster

WORKDIR /app

COPY . .

ENV PYTHONPATH "/app/src"
RUN pip install -r requirements.txt

EXPOSE 9090

CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0","--port", "9090","--reload"]