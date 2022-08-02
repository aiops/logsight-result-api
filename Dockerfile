# docker build -t logsight/logsight-result-api .

# set base image (host OS)
FROM python:3.8-slim

ARG GITHUB_TOKEN
ARG LOGSIGHT_LIB_VERSION

RUN apt-get update && \
    apt-get -y install --no-install-recommends libc-bin openssh-client git-lfs && \
    rm -r /var/lib/apt/lists/*

ENV LDFLAGS="-L/usr/lib/x86_64-linux-gnu"
ENV CFLAGS="-I/usr/include"

# set the working directory in the container
WORKDIR /code

COPY requirements.txt .
# install dependencies
RUN pip install -r requirements.txt

RUN pip install "git+https://$GITHUB_TOKEN@github.com/aiops/logsight.git@$LOGSIGHT_LIB_VERSION"


# copy code
COPY result_api/ result_api
# copy entrypoint.sh
COPY entrypoint.sh .

# Set logsight home dir
ENV LOGSIGHT_HOME="/code/result_api"
ENV PYTHONPATH="/code"
EXPOSE 5554

ENTRYPOINT [ "./entrypoint.sh" ]
