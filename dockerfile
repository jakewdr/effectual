FROM python:3.11.10-alpine3.20

ADD dist/bundle.py .

CMD ["python", "./bundle.py"]