FROM nvidia/cuda:10.1-devel-ubuntu18.04

COPY sdk /sdk
ENV PYTHON_GET_PIP_URL=https://bootstrap.pypa.io/get-pip.py 

RUN cd /etc/apt/sources.list.d && mv nvidia-ml.list .. && mv cuda.list .. && \
    apt-get update && apt-get install python3.7 python3-distutils -y --no-install-recommends && \ 
    cd /usr/bin && ln -s python3.7 python && \
    apt-get install -y --no-install-recommends wget; wget -O get-pip.py "$PYTHON_GET_PIP_URL"; python get-pip.py --disable-pip-version-check --no-cache-dir "pip==19.3"; rm -f get-pip.py && \
    pip install -r /sdk/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ && \
    useradd -m -G staff -N tester -p tester
