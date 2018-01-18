HIRMEOS Altmetrics (WP6)
========================

This project implements the HIRMEOS Work Package 6.

How to run the service
----------------------

Locally
.......

.. code-block:: bash

    cp config.ini local.ini

Edit the ``config.ini`` file, filling in the credentials for your local / dev
environment.

.. code-block:: bash

    cd src
    ./manage.py migrate --settings=core.settings_dev
    ./manage.py collectstatic --settings=core.settings_dev
    ./manage.py runserver --settings=core.settings_dev

In production
.............

.. code-block:: bash

    cp config.ini local.ini

Edit the ``config.ini`` file, filling in the credentials for your production
environment.

.. code-block:: bash

    cd src
    ./manage.py migrate
    ./manage.py collectstatic
    ./manage.py runserver
