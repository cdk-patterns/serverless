FROM amazonlinux:2

WORKDIR /app

# Install binaries dependencies
RUN yum install -y \
    python3-pip \
    python3 \
    python3-setuptools \
 && yum clean all \
 && rm -rf /var/cache/yum

# Install app dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Install application
COPY main.py .

ENTRYPOINT [ "python3", "/app/main.py" ]
# CMD ["python3", "./server.py"]