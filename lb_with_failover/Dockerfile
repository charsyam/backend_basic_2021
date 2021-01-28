FROM python:3.8-alpine
MAINTAINER CharSyam "charsyam@gmail.com"
COPY app /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
