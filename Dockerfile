FROM ubuntu
MAINTAINER N. Mauchle <me@nicolasmauchle.ch>

RUN apt-get update && apt-get upgrade -y && apt-get install -y build-essential libgmp3-dev zlib1g-dev  libreadline-dev python3 cython3 libncurses5-dev git

ADD scipoptsuite-3.2.1.tgz /root

WORKDIR /root/scipoptsuite-3.2.1

RUN make -j6 && make -j6 SHARED=true GMP=false READLINE=false scipoptlib && make -j6 install INSTALLDIR="../../usr/local"
RUN make -j6 && make -j6 install INSTALLDIR="../../usr/local"
WORKDIR /root/
RUN git clone https://github.com/SCIP-Interfaces/PySCIPOpt.git

WORKDIR /root/PySCIPOpt
RUN env SCIPOPTDIR=/root/scipoptsuite-3.2.1 python3 setup.py install

# from pyscipopt import Model
