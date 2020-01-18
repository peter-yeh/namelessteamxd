# nameless-team
For hack n roll 2019

## Setup

### System Requirements
1. Python (>= 3.6.5)
1. Pip (>= 19.2.2)
1. virtualenv (== 16.0.0)
1. MariaDB (>= 10.4.8)
1. python-telegram-bot (>= 12.3.0)

### Getting Started

 1. Install Python Dependencies

    ```
    $ pip install -r requirements.txt
    ```

 2. Create and seed the database (Create a database named `recipefinder` in mysql first)
    ```
    $ python manage.py migrate
    ```

 3. Run the webserver
    ```
    $ python manage.py runserver

### Setting up in Virtual Environment

 1. Setup Virtual Environment
    ```
    $ python -m venv virtualenv
    ```

 2. Activate Virtual Environment
    ```
    $ .\virtualenv\Scripts\activate
    ```

 3. Update pip to latest version
    ```
    $ python -m pip install --upgrade pip
    ```

 4. Repeat the above steps to set up the project in the virtual environment
    Run the following code to deactivate the virtual environment
    ```
    $ deactivate
    ```

 Note: Run all future commands after activating virtual environment to ensure consistencies