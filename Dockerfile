# docker build -t logsight/logsight-result-api .

# set base image (host OS)
FROM python:3.7-slim

ENV LDFLAGS="-L/usr/lib/x86_64-linux-gnu"
ENV CFLAGS="-I/usr/include"

# set the working directory in the container
WORKDIR /code

COPY requirements.txt .
# install dependencies
RUN pip install -r requirements.txt

# copy code
COPY result_api/ result_api
# copy entrypoint.sh
COPY entrypoint.sh .

# Set logsight home dir
ENV LOGSIGHT_HOME="/code/result_api"

ENTRYPOINT [ "./entrypoint.sh" ]
