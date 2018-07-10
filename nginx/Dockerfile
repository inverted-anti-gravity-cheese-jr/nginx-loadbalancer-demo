from nginx:latest

copy nginx.conf /etc/nginx/nginx.conf

run mkdir -p /opt/app/ssl
copy ssl/ /opt/app/ssl/

run mkdir -p /etc/nginx/logs

expose 81
