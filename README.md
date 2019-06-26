# finacompare-challenge

This project is a simple project which has 2 parts:

1- A feeder which reads data from a csv file and 
send its data to a queue.

2- A consumer which follows the queue to save the data in the database.

## Technologies

- Queue: 'Rabbitmq' for queueing and 'Pika' for working with 'Rabbitmq' in python
- Framework: 'Django' to handle database models and migrations which makes the project independent from database technology.


## How to run

1- Clone the project

2- Create virtual environment using python3.

    virtualenv -p python3 env
    
3- Activate virtual environment.

    source env_name/bin/activate

4- Install requirements.
    
    pip install -r requirements.txt

5- Install RabbitMQ in your system. See here: https://www.rabbitmq.com/download.html

6- Install Postgres on your system. You can install any database, in this case we provide help to use postgres.

7- Create user for project in postgres with any desirable password.
    
    createuser fincompare -P
    
you can set any username and password.

8- Create project db in postgres.
    
    createdb fincampare-challenge --owner=fincompare
    
You can name the db any name you want.

9- Create a file local_settings.py using local_settings_sample and fill the db information with the created db information.

10- Run migrations.

    python manage.py migrate

    
11- To run feeder, place data csv file in the root of project and run this command at the root of project.

    python manage.py read_data
    

12- To run consumer, run the following command at the root of project. 
    
    python manage.py consume

Run this command as many time as the number of clients for processing the queue you need.


    