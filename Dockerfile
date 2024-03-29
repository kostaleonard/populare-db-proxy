FROM python:3.9-alpine
EXPOSE 8000
WORKDIR /app
COPY . .
RUN apk update && \
    apk add --no-cache make && \
    make install
ENTRYPOINT ["make", "run"]
