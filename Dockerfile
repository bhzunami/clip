FROM ubuntu
MAINTAINER N. Mauchle <me@nicolasmauchle.ch>

RUN apt-get update && apt-get upgrade -y && apt-get install -y build-essential libgmp3-dev zlib1g-dev  libreadline-dev python3 cython3 libncurses5-dev git python3-setuptools wget python3-pip python3-tk

# For version 3.2.1
#ADD scipoptsuite-3.2.1.tgz /root
#WORKDIR /root/scipoptsuite-3.2.1
# Use newest version
ADD scipoptsuite-4.0.0.tgz /root
WORKDIR /root/scipoptsuite-4.0.0

RUN make -j6 && make -j6 SHARED=true GMP=false READLINE=false scipoptlib  && make -j6 install INSTALLDIR="../../usr/local" SHARED=true GMP=false READLINE=false scipoptlib

WORKDIR /root/

# RUN wget https://github.com/SCIP-Interfaces/PySCIPOpt/archive/v0.1-SCIP-3.2.1.tar.gz && tar -xzf /root/v0.1-SCIP-3.2.1.tar.gz
# WORKDIR /root/PySCIPOpt-0.1-SCIP-3.2.1/
#RUN env SCIPOPTDIR=/root/scipoptsuite-3.2.1 python3 setup.py install

RUN git clone https://github.com/SCIP-Interfaces/PySCIPOpt.git
WORKDIR /root/PySCIPOpt/
RUN env SCIPOPTDIR=/root/scipoptsuite-4.0.0 python3 setup.py install

# Install Pip3 packages
RUN pip3 install psutil memory_profiler line_profiler objgraph numpy scipy pytest networkx matplotlib
