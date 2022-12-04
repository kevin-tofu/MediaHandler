ARG registry=test
FROM python:3.8.10-slim-buster

WORKDIR /myapp
COPY ./ ./
COPY ./requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install .

EXPOSE 80
CMD ["python", "./server.py"]