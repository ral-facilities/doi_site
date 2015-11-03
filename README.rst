Introduction
============

This code provides a shim layer in front of the Datacite API in order to apply
local security settings, limiting the sub-domain for which a user can mint
DOIs. It is designed to hook into a sites LDAP server in order to authenticate
users.

Installation and Configuration
==============================

Prerequisites
-------------

- Python => 2.7
- python-virtualenv
- gcc
- mod_ssl.x86_64
- mod_wsgi.x86_64
- openldap-devel
- Apache

Installation
------------

Create the directory for the static files

.. code:: bash

    mkdir -p /var/www/html/doi

Create the directory for the sqlite database

.. code:: bash

    mkdir -p /var/doi

Create the python virtual environment

.. code:: bash

    cd /opt
    virtualenv doi
    cd doi
    source bin/activate
    export DJANGO_PROJECT_STATIC_FILES=/var/www/html/doi/


Local customisation for proxy, if required

.. code:: bash

    export http_proxy=http://example.org:8080
    export https_proxy=http://example.org:8080
    
Install the software

.. code:: bash

    pip install doi_site

Configuration
-------------

local_settings.py
^^^^^^^^^^^^^^^^^
Create a copy of the ``local_settings.py.ini`` file as ``local_settings.py``
Review the contents of this file and update the parameters. You MUST provide values for:

- ``DOI_PREFIX``
- ``DATACITE_USER_NAME``
- ``DATACITE_PASSWORD``
- ``AUTH_LDAP_SERVER_URI``
- ``AUTH_LDAP_USER_DN_TEMPLATE``
- ``ORGANISATION_NAME``
- ``ORGANISATION_DOI_EMAIL``
- ``SECRET_KEY``
- ``ALLOWED_HOSTS``

You should provide values for:

- ``ROLES_URL``
- ``NOTES_URL``

Additionally if necessary provide values for:

- ``HTTP_PROXY_HOST``
- ``HTTP_PROXY_PORT``

By default the DataCite ``TEST`` MDS is used. To use the ``PRODUCTION`` MDS uncomment:

- ``DATACITE_URL``
- ``DATACITE_HANDLER``

In a testing environment you can set ``DEBUG = True``

Initialisation and Admin User Creation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

    python lib/python2.7/site-packages/doi_site/manage.py collectstatic --clear --noinput
    python lib/python2.7/site-packages/doi_site/manage.py syncdb --noinput
    python lib/python2.7/site-packages/doi_site/manage.py createsuperuser
    deactivate

Stuff for apache
^^^^^^^^^^^^^^^^

.. code:: bash

    cp -p  /opt/doi/lib/python2.7/site-packages/doi_site/resources/doi_wsgi.conf /etc/httpd/conf.d/

Assuming apache is running as the user ``apache``

.. code:: bash

    chown -R apache /opt/doi
    chown -R apache /var/doi
    
    systemctl start httpd
    

Customisation of the Web Pages
==============================

This code makes use of inheritance within the templates. It has been structured to make it relatively easy to customise the look and feel of the site. Everything inherits from base.html.

base.html -> organisation_wrapper.html -> everything else

To customise the appearance of the site provide your own ``organisation_skin.html``, which should inherit from ``base.html``.
Change ``organisation_wrapper.html`` to inherit from your ``organisation_skin.html``

base.html -> organisation_wrapper.html -> organisation_wrapper.html -> everything else

Within your ``organisation_skin.html`` you can override the following blocks:

- head
- page_header
- navbar
- content
- footer

Place any css files in the directory ``static/doi_site/css/``

If you have made any changes you will have to restart apache

Adding DOI Domains via the Admin Web Page
=========================================

In a browser go to the admin pages, i.e. ``https://example.org/admin/``

You will need you credentials that you used to create the superuser to log on

Click on ``+Add`` besides the ``Groups`` label

Give a name to the group and a DOI suffix

Save your changes


Granting Minting Privileges to Users
====================================

Get the user to log in with their LDAP username and password, this will create a local account (the password is not stored in the django database).

In a browser go to the admin pages, i.e. ``https://example.org/admin/``

You will need you credentials that you used to create the superuser to log on

Click on ``Users``

Click on the user name you wish to edit

Fill in their personal information, first name, last name, email address

Within the ``Groups`` in the ``Permissions`` section, assign the user to the required groups

Save the changes

They will then be able to mint DOIs for that groups DOI prefix
