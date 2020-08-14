FROM ubuntu
RUN echo "This is a Ubuntu image with gcc,g++,python3"
RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y g++
RUN apt-get install -y python3
RUN mkdir /home/code
RUN cd /home/code
CMD /bin/bash
VOLUME ["/home/code"]
WORKDIR /home/code