import pika
import logging

from django.conf import settings

logger = logging.getLogger(__name__)


class QChannel:
    def __init__(self, q_name):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBIT_CONNECTION_HOST))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=q_name, durable=True)  # queue would be safe if rabbit shuts down by durability
        self.q_name = q_name
        self.channel.basic_qos(prefetch_count=1)  # prevent having some busy queues while others have ended their tasks
        # by sending the tasks one by one

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.connection.close()

    def send_message(self, q_name, message):
        self.channel.basic_publish(exchange='',
                                   routing_key=q_name,
                                   body=message,
                                   properties=pika.BasicProperties(
                                       delivery_mode=2,  # make message persistent in case shut downs and other problems
                                   ))
        logger.info(f'{message} sent to queue {self.q_name}')

    def start_receiving(self, callback):  # this will run forever and can be terminated manually
        self.channel.basic_consume(
            queue=self.q_name, on_message_callback=self.receiver_callback(callback))
        logger.info('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def receiver_callback(self, callback):
        def res(channel, method, properties, body):
            logger.info(f'{body} received to queue {self.q_name}')
            try:
                callback(channel, method, properties, body)
                channel.basic_ack(delivery_tag=method.delivery_tag)  # the queue would remove a task
                # after getting acknowledgement
                logger.info(f'{body} has been proceeded successfully.')
            except Exception as ex:
                logger.error(ex)
                # In case of exception in running call back, We retry the task by nack. But if the task is redelivered,
                # we skip it and sending ack.
                # todo: we can add some feature to support specified time retrying the failures.
                if not method.redelivered:
                    logger.info(f'message {body} has been requeued')
                    channel.basic_nack(delivery_tag=method.delivery_tag)
                else:
                    channel.basic_ack(delivery_tag=method.delivery_tag)

        return res
