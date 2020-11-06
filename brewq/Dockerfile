FROM rabbitmq:3.8-alpine

COPY rabbitmq.conf /etc/rabbitmq/

ENV LVC_VERSION=3.8.0
RUN set -ex \
        && printenv \
        && apk add ca-certificates wget \
        && update-ca-certificates \
        && wget -O /plugins/rabbitmq_lvc_exchange-${RABBITMQ_VERSION}.ez \
        https://github.com/rabbitmq/rabbitmq-lvc-exchange/releases/download/v${LVC_VERSION}/rabbitmq_lvc_exchange-${LVC_VERSION}.ez \
        && apk del ca-certificates wget

RUN rabbitmq-plugins enable --offline rabbitmq_lvc_exchange rabbitmq_web_mqtt
