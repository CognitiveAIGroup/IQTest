FROM model-base:v-slim 

COPY sdk /install_package 
RUN cd /install_package && \
    tar -xf iqtestsdk-0.2.4.4.tar.gz && \
    cd iqtestsdk-0.2.4.4 && \
    pip install . && \
    rm -rf /install_package 

