# SetupFAQ
We are here, to help you to get everything configured swimmingly.

### Set up project locally
Prerequisite
1. Python 3.7
2. PostgreSQL 10
 
**Steps to configure and run the project**
1. Create a virtual environment.
2. Initialise pre-commit hook:
    ```bash
    pip install pre-commit && \
    pre-commit install && \
    export LC_ALL=en_US.UTF-8; export LANG=en_US.UTF-8 
    ```
3. Install required packages:
    ```bash
    pip install -r requirements.txt
    pip install -r requirements.dev.txt
    ```
4. Add `.env` file to the project you can refer `.env.template`. 
5. Make database migrations: 
    1. ***Note***: Create a DB (with same name that you have been added in the .env file) first in PostgreSQL before making migrations. 
    ```bash
    ./manage.py makemigrations
    ./manage.py migrate
    ```
6. Create a super user to access Django Admin panel:  
    ```bash
    ./manage.py createsuperuser
    ```
7. Finally, run the project:  
    ```bash
    ./manage.py runserver
    ```
 
***Note***: Always execute the below command before commiting your changes on GitHub: 
```bash
./manage.py collectstatic
```
    
### References
1. [JS library: showdown for rendering md files](https://github.com/showdownjs/showdown)
2. [Showdown demo](http://demo.showdownjs.com/)
3. [Python Markdown package demo](https://github.com/Python-Markdown/markdown/wiki/Tutorial:-Writing-Extensions-for-Python-Markdown)
4. [Django Book](https://django-book.readthedocs.io/en/latest/index.html)
5. [Migrations Issue](https://stackoverflow.com/questions/29253399/how-to-reset-migrations-in-django-1-7)
6. [CKEditor Docs](https://libraries.io/github/django-ckeditor/django-ckeditor)
7. [Privacy Policy Generator](https://www.privacypolicygenerator.info/)
