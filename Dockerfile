ARG registry=test
FROM python:3.8.10-slim-buster

WORKDIR /myapp
COPY ./ ./
COPY ./requirements.txt ./


RUN apt-get update -y
RUN apt-get upgrade -y
# ImportError: libGL.so.1: cannot open shared object file: No such file or directory
# ImportError: libgthread-2.0.so.0: cannot open shared object file: No such file or directory
# RUN apt-get install libgl1-mesa-dev -y
RUN apt-get install libopencv-dev -y 

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install .
RUN pip install numpy==1.19.3 opencv-python==4.6.0.66

EXPOSE 80
CMD ["python", "./server.py"]