FROM sagemath/sagemath

MAINTAINER Langston Barrett <langston.barrett@gmail.com>

USER root
RUN [ "apt-get", "update", "-qq" ]
RUN [ "apt-get", "install", "-y", "-qq", "unzip" ]

# Python dependencies
USER sage
ENV HOME /home/sage
RUN [ "sage", "--pip", "install", "pytest", "pytest-runner", "pytest-benchmark" ]
RUN [ "sage", "--pip", "install", "hypothesis" ]

# Get CHOMP
RUN [ "mkdir", "-p", "/tmp/chomp" ]
WORKDIR /tmp/chomp
RUN [ "wget", "--quiet", "chomp.rutgers.edu/Projects/Computational_Homology/OriginalCHomP/download/chompfull_deb64.zip" ]
RUN [ "unzip", "chompfull_deb64.zip" ]
ENV PATH $PATH:/tmp/chomp/bin

WORKDIR /home/sage
ENV PYTHONPATH $PYTHONPATH:/home/sage

CMD [ "sage" ]
