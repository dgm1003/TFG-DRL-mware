FROM alpine:3.10.1

RUN apk add python3 && \
    apk add py3-pip

RUN apk add --no-cache --update \
    python3 python3-dev gcc \
    gfortran musl-dev g++ \
    libffi-dev openssl-dev \
    libxml2 libxml2-dev \
    libxslt libxslt-dev \
    libjpeg-turbo-dev zlib-dev \
    gcc build-base \
    freetype-dev \
    libpng-dev \
    openblas-dev

COPY websiteCode/* /tfg/

WORKDIR /tfg

RUN mkdir frontendContents
RUN mkdir backendContents

RUN cp endpoints.py frontendContents/
RUN cp agente_web.py entorno_web.py backendContents/

RUN pip3 install -U pip

RUN pip3 install -r requirements.txt

RUN ls

ENTRYPOINT python3 frontendEndpoints.py