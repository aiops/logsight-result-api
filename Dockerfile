# docker build -t logsight/logsight-result-api .

# set base image (host OS)
FROM python:3.8-slim

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

RUN mkdir -p -m 0700 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
RUN --mount=type=ssh pip install git+ssh://git@github.com/aiops/logsight.git@lib#egg=logsight

# copy code
COPY result_api/ result_api
# copy entrypoint.sh
COPY entrypoint.sh .

# Set logsight home dir
ENV LOGSIGHT_HOME="/code/result_api"
ENV PYTHONPATH="/code"
EXPOSE 5554

ENTRYPOINT [ "./entrypoint.sh" ]
