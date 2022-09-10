FROM python:3.10

COPY ./server /app
COPY ./wait-for-it.sh /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN pip install -e .

# Wait for the database to be ready
RUN chmod +x ./wait-for-it.sh
CMD ["./wait-for-it.sh", "postgres:5432", "-t", "20", "--", "gunicorn", "-b", "0.0.0.0:8080", "src.main:app"]
