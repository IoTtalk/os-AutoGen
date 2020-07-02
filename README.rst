IoTtalk AutoGen Subsystem
======================================================================


Installation
----------------------------------------------------------------------

Install required package
::

    pip install -r requirements.txt
    pip install git+https://gitlab.com/IoTtalk/ccmapi-py.git

Migrate database
::

    python manage.py makemigrations autogen
    python manage.py migrate

