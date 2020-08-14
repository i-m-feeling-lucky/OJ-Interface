FROM ubuntu
RUN echo "This is a Ubuntu image with gcc,g++,python3" && \
    apt-get update && \
    apt-get install -y gcc g++ python3 && \
    mkdir -p /home/code
CMD ["/bin/bash"]
VOLUME ["/home/code"]
WORKDIR /home/code
