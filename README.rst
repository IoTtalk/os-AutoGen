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

Modify Config file, set the ccm host to your iottalk-ccm server. 
::
    # autogen/config.py
    ccm_api_url = 'http://<CCM_HOST>[:<CCM_PORT>]/api/v0'
