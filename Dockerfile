FROM python:3.12.11-alpine

# set work directory
WORKDIR /usr/src/app

# Add required repositories for GDAL
RUN apk update && \ 
    apk add --no-cache \
    --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
    --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
    libmaxminddb \
    postgresql-dev \
    gcc \
    musl-dev \
    gdal-dev \
    geos-dev \ 
    linux-headers \
    g++ \
    && \
    rm -rf /var/cache/apk/* # Clean up package cache


# copy project
COPY entrypoint.sh gunicorn.cfg.py pytest.ini /usr/src/app/
COPY src/ /usr/src/app

# install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache -r requirements.txt

#PORT
EXPOSE 8000

CMD ["sh","entrypoint.sh"]