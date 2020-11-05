# Base image
FROM php:5.6-fpm-alpine

LABEL Organization="CISCN 2020 Final"
MAINTAINER "unc1e"

# ssh的密码
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
&& apk add --update --no-cache nginx 


# 题目处理
# copy and extract src 
ADD ./src/* /var/www/html/
ADD ./_files/* /tmp/

# src code AND mysql
RUN mkdir /run/nginx \
    && mv /tmp/docker-php-entrypoint /usr/local/bin/docker-php-entrypoint \
    && chmod +x /usr/local/bin/docker-php-entrypoint \
    && mv /tmp/nginx.conf /etc/nginx/nginx.conf \
    && chown -R www-data:www-data /var/www/html/ 
# config
WORKDIR /var/www/html/

# CMD ["/bin/sh", "-c", "docker-php-entrypoint"]
ENTRYPOINT ["/bin/sh", "-c", "docker-php-entrypoint"]
