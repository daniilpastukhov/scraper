FROM ubuntu

COPY ./scraper /app
COPY ./wait-for-it.sh /app
WORKDIR /app

RUN apt-get update -y && \
#    apt-get upgrade -y && \
    apt-get install -y python3-pip libpq-dev

RUN pip install -r requirements.txt && \
    pip install -e .

RUN playwright install-deps && \
    playwright install chromium

# Wait for the database to be ready
RUN chmod +x ./wait-for-it.sh
CMD ["./wait-for-it.sh", "postgres:5432", "-t", "20", "--", "scrapy", "crawl", "sreality"]