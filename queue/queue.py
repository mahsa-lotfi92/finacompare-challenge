import pika

# todo: for a real product, maybe it would be better to use celery for managing rabbitmq.
# Since celery provides more ability to manage and handle many more complex situations.


class QChannel:
    def __init__(self, q_name):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=q_name, durable=True)
        self.q_name = q_name
        self.channel.basic_qos(prefetch_count=1)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.connection.close()

    def send_message(self, q_name, message):
        self.channel.basic_publish(exchange='',
                                   routing_key=q_name,
                                   body=message,
                                   properties=pika.BasicProperties(
                                       delivery_mode=2,  # make message persistent
                                   ))
        print(f'{message} received in queue {self.q_name}')

    def receive(self, callback):
        self.channel.basic_consume(
            queue=self.q_name, on_message_callback=callback)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    @staticmethod
    def receiver_callback(callback):
        def res(*args, **kwargs):
            print(" [x] Received %r" % args[3])
            callback(*args, **kwargs)
            args[0].basic_ack(delivery_tag=args[1].delivery_tag)

        return res
