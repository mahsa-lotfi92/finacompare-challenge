DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fincompare-challenge',
        'USER': 'fincompare',
        'PASSWORD': 'fincompare',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

RABBIT_CONNECTION_HOST = 'localhost'
RABBITMQ_QUEUE_NAME = 'emails'
