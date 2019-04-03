HIRMEOS Altmetrics (WP6)
========================

This project implements the HIRMEOS Work Package 6.

How to run the service
----------------------


Set up a virtual environment
............................

.. code-block:: bash

    $ mkvirtualenv wp6-altmetrics --python=/usr/bin/python3.7

In this venv, install the project requirements.

.. code-block:: bash

    $ pip install -r requirements.txt

For development work, rather install the dev-requirements.

.. code-block:: bash

    $ pip install -r requirements-dev.txt


Setting environmental variables
...............................

The bash script, **flask_local.bash** can be used to set environmental variables
needed by the flask app when running the Altmetrics service.

These environmental variables are needed by various external services used by
the Altmetrics service. These will be described below. Please remember to update
the bash script with any credentials you create when setting up these services.

It is recommended that you create an alias to run this script, as follows:

.. code-block:: bash

    $ alias altmetrics="path/to/flask_local.bash flask"

    $ alias altmetrics-celery="path/to/flask_local.bash celery"

This way the flask service can be run with the 'altmetrics' command. The
examples given below, assume you have created this alias. This should be run
from the **src** directory.

Without any further changes, you should be able to run the following command
to get an interactive Python shell for flask.

.. code-block:: bash

    $ altmetrics shell


The following command can be used to run the application (though it won't be
completely functional until you have completed some of the steps below).

.. code-block:: bash

    $ altmetrics run


Set up a database
.................

The Altmetrics service has been written to use PostgreSQL. You will need to
create a database instance, as well as a user who can access this database
before continuing.

The example below is written for Ubuntu. Please refer to the PostgreSQL
documentation for this process using MacOS or other Linux distributions.

.. code-block:: bash

    $ sudo -u postgres createdb altmetrics_db
    $ sudo su - postgres
    $ createuser altmetrics_user --pwprompt

    $ sudo su - postgres
    $ psql

    # ALTER DATABASE altmetrics_db OWNER TO altmetrics_user;


**Remember to update the flask_local.bash script with these credentials.**

Once you have a database, you can use the following command to create the tables
used by the Altmetrics service and apply any migrations.

.. code-block:: bash

    $ altmetrics db upgrade


Create an admin user
....................

In future, this will be done automatically, based on environmental variables,
but for now, you will need to do the following:


.. code-block:: bash

    $ altmetrics shell      #ipython flask shell

    In [1]: from core.scripts.create_admin import create_admin
    In [2]: create_admin()

Then follow the command prompts. This user will have admin privileges so they
can access the admin site.


Setting up RabbitMQ
...................

Asynchronous tasks are scheduled and executed using RabbitRM. For local
development, it should be sufficient to use the official RabbitMQ management
docker image.

.. code-block:: bash

    $ docker run -d --hostname localhost --name docker-rabbit \
        -e RABBITMQ_DEFAULT_USER=user \
        -e RABBITMQ_DEFAULT_PASS=password \
        -e RABBITMQ_DEFAULT_VHOST=altmetrics \
        -p 5672:5672 \
        -p 15672:15672 \
        rabbitmq:3-management


Celery tasks
............

While RabbitMQ is running, you can use the following command to enable celery
tasks to be run:

.. code-block:: bash

    altmetrics-celery -A core.celery.celery worker -l info \
        -Q altmetrics.pull-metrics,altmetrics.approve-user,altmetrics.send-approval-request \
        --hostname=altmetrics@localhost \
        -B

**Note:** You will need to terminate this process and restart it if you make any
changes to the code for the celery tasks.



Mailgun
.......

Mailgun is used to send emails during the user registration process. Please
refer to Mailgun's documentation to set up an account, and update the
**flask_local.bash** script with your mailgun credentials.

Sending emails is not strictly necessary when running the Altmetrics service
locally. If you are unable to set up a mailgun account, then registering for
the Altmetrics service will cause the site to crash, but a user will still be
created, and you can approve them in the admin interface.


Twitter
.......

In order to use the twitter plugin, you will need a Twitter developer account.
Please refer to Twitter's documentation to set up an account, and update the
**flask_local.bash** script with your credentials.


Running tests
.............

Tests for the Altmetrics service have been written using unittest. To run tests,
execute the following command from the **altmetrics/src** directory:

.. code-block:: bash

    $ python -m unittest discover core.tests -t . -v


Credits
-------

* OPERAS / HIRMEOS for having funded, supported and advised the development
* Marty Alchin and Régis Décamps for the `KISS plugin architecture`_


.. _KISS plugin architecture: https://github.com/regisd/simple_plugin_framework
