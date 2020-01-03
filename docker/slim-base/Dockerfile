FROM python:3.7.4-slim

COPY sdk /sdk
RUN apt-get update && \
    pip install -r /sdk/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ && \
    useradd -m -G staff -N tester -p tester
