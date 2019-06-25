from feeder.application.reader import Reader

if __name__ == '__main__':
    Reader('emails').file_to_queue('data_example.csv')