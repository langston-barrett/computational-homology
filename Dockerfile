FROM sagemath/sagemath

MAINTAINER Langston Barrett <langston.barrett@gmail.com>

USER root
RUN [ "apt-get", "update", "-qq" ]
RUN [ "apt-get", "install", "-y", "-qq", "graphviz" ]

USER sage
ENV HOME /home/sage
WORKDIR /home/sage
RUN [ "sage", "--pip", "install", "pytest", "pytest-runner", "pytest-benchmark" ]
RUN [ "sage", "--pip", "install", "hypothesis" ]

ENV PYTHONPATH $PYTHONPATH:/home/sage

CMD [ "sage" ]
