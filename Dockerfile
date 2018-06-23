FROM lokeshgupta/client-python-kubernetes
MAINTAINER Lokesh Gupta <lokeshgupta13@gmail.com>

ADD controller.py /tmp
ADD splunkindex.yml /tmp

ENTRYPOINT  ["python", "-u", "/tmp/controller.py"]
