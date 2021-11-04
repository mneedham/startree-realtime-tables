FROM openjdk:11

WORKDIR /app

ENV PINOT_VERSION=0.8.0

RUN wget https://downloads.apache.org/pinot/apache-pinot-$PINOT_VERSION/apache-pinot-$PINOT_VERSION-bin.tar.gz
RUN tar -zxvf apache-pinot-$PINOT_VERSION-bin.tar.gz
RUN mv apache-pinot-$PINOT_VERSION-bin pinot

RUN curl -fsSL https://deb.nodesource.com/setup_14.x | bash -
RUN apt install nodejs
RUN npm install eventsource kafkajs

RUN mkdir -p /app/realtime/events
COPY wikievents.js /app/realtime
COPY pinot /app/realtime/pinot

RUN wget https://mirrors.ocf.berkeley.edu/apache/kafka/2.8.1/kafka_2.13-2.8.1.tgz
RUN tar -xvf kafka_2.13-2.8.1.tgz
RUN mv kafka_2.13-2.8.1 kafka
COPY kafka/server.properties /app/kafka/config/

EXPOSE 9000
EXPOSE 8000
EXPOSE 8099