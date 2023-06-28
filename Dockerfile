FROM python:3.8.17-alpine

RUN apk add vim curl --no-cache && \
    pip install flask requests prometheus_client

WORKDIR /opt

EXPOSE 5000

COPY ./app.py /opt/app.py

CMD ["python", "app.py"]