import pika
import logging

logger = logging.getLogger(__name__)


class QChannel:
    def __init__(self, q_name):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
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
        logger.info(f'{message} received in queue {self.q_name}')

    def receive(self, callback):
        self.channel.basic_consume(
            queue=self.q_name, on_message_callback=callback)
        logger.info('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    @staticmethod
    def receiver_callback(callback):
        def res(*args, **kwargs):
            logger.info(f'Received {args[3]}')
            callback(*args, **kwargs)
            args[0].basic_ack(delivery_tag=args[1].delivery_tag)  # the queue would remove a task
            # after getting acknowledgement

        return res
