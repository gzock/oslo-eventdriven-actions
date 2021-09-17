FROM gzock/ansible-for-openstack:latest

RUN pip3 install oslo.messaging

WORKDIR /usr/local/oslo-eventdriven-actions/
ADD ./ ./
ENTRYPOINT ["python3", "main.py"]
