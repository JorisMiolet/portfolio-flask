FROM python:3.11.7

WORKDIR /app

COPY . /app

RUN pip install flask

EXPOSE 5000

CMD ["flask","run","--host=0.0.0.0", "--port=5000"]