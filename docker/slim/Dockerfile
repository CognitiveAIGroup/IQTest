FROM iqtest/model-base

COPY sdk /install_package 
RUN pip install -r /install_package/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ && \
    cd /install_package && \
    tar -xf iqtestsdk-0.2.5.1.tar.gz && \
    cd iqtestsdk-0.2.5.1 && \
    pip install . && \
    rm -rf /install_package 

