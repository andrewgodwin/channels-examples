#!/bin/bash
set -e

function rabbitmq_ready {
    python << END
import sys
import pika
import pika.exceptions
try:
    conn = pika.BlockingConnection(
        pika.ConnectionParameters(
            '$RABBITMQ_HOST', 5672, '/', pika.PlainCredentials('guest', 'guest')
        ),
    )
except pika.exceptions.ConnectionClosed:
    sys.exit(-1)
sys.exit(0)
END
}

until rabbitmq_ready
do
    echo "RabbitMQ is unavailable - sleeping"
    sleep 1
done

echo "RabbitMQ is up - continuing..."
exec "$@"
