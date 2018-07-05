from centos:latest

run yum -y install epel-release
run yum -y update
run yum -y install python python-pip

run pip install flask
run pip install redis
run mkdir -p /opt/app/templates

copy main.py /opt/app/
copy templates/* /opt/app/templates/

expose 5000

entrypoint ["python"]
cmd ["/opt/app/main.py"]
