# docker build -t logsight/logsight-result-api .

# set base image (host OS)
FROM python:3.8

ARG GITHUB_TOKEN
ARG LOGSIGHT_LIB_VERSION

ENV GITHUB_TOKEN="GIT_TOKEN"
ENV LOGSIGHT_LIB_VERSION="v1.3.0"
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

RUN echo $GITHUB_TOKEN
RUN apt-get update && \
    apt-get -y install --no-install-recommends git-lfs && \
    rm -r /var/lib/apt/lists/*

ENV LDFLAGS="-L/usr/lib/x86_64-linux-gnu"
ENV CFLAGS="-I/usr/include"

# set the working directory in the container
WORKDIR /code

COPY requirements.txt .
# install dependencies
RUN pip install -r requirements.txt

RUN pip install "git+https://$GITHUB_TOKEN@github.com/aiops/logsight.git@$LOGSIGHT_LIB_VERSION"

RUN pip install "git+https://$GITHUB_TOKEN@github.com/ncktl/logcheck.git@pip"

# copy code
COPY result_api/ result_api
# copy entrypoint.sh
COPY entrypoint.sh .

# Set logsight home dir
ENV LOGSIGHT_HOME="/code/result_api"
ENV PYTHONPATH="/code"
EXPOSE 5554

ENTRYPOINT [ "./entrypoint.sh" ]
