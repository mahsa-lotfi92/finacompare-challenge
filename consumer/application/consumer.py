from queue.queue import QChannel


if __name__ == '__main__':
    @QChannel.receiver_callback
    def callback(ch, method, properties, body):
        pass

    QChannel('emails').receive(callback)

