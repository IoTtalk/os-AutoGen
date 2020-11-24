IoTtalk AutoGen Subsystem
======================================================================


Installation
----------------------------------------------------------------------

Install required package
::

    pip install -r requirements.txt

Migrate database
::

    python manage.py makemigrations autogen
    python manage.py migrate

Modify Setting file, set the ccm host to your iottalk-ccm server.
::
    # autogen/settings.py
    ccm_api_url = 'http://<CCM_HOST>[:<CCM_PORT>]/api/v0'
