from centos:latest

run yum -y install epel-release
run yum -y update
run yum -y install redis

expose 6379

cmd ["redis-server", "--protected-mode", "no"]
