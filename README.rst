=======
MiniERP
=======

MiniERP is a simple Django app to ...

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "minierp" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'minierp',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^minierp/', include('minierp.urls')),

3. Run `python manage.py migrate` to create the minierp models.

4. Start the development server and visit http://127.0.0.1:8000/minierp.
