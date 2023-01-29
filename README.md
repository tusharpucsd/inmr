### Setting up and Running the Project in Python

Pull Requests
-------------
https://github.com/tusharpucsd/inmr.git

# Prerequisites
- Python
- MySQL
- mysql connector

Create and activate Virtual Environment::

    # With virtualenv
    $ python -m venv inmar_venv
    $ source inmar_venv/bin/activate

Install requirements::

    $ cd inmar
    $ pip install -r requirements.txt
    
Create Database and do migrations::

    $ create database sku;
    $ python manage.py makemigrations
    $ python manage.py migrate
    
Load data through management commands::

    $ python manage.py importdata sku\meta_data.csv
    $ python manage.py loadskudata sku\sku_data.txt
    
Run the development server::

    $ python manage.py runserver 0.0.0.0:8000


    
  

