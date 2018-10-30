FROM ubuntu:latest

RUN apt-get update -y && apt-get install -y python-pip python-dev build-essential
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["app.py"]
