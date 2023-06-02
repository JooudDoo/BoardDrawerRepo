
FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY assets ./assets
COPY src ./src

RUN echo "Running tests"
RUN python src/test/test_maintainer.py
RUN echo "Launching an application"
CMD ["python", "src/main.py"]