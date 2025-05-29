# Django APP for Smart Expense Tracker

**Dependencies**

https://github.com/Aniket-0411/expenseTrackerFrontend

https://github.com/Aniket-0411/expenseTrackerBackend

...existing code...

## Installation

1. Create a virtual environment:
   ```
   python -m venv venv
   ```
2. Activate the virtual environment:
   - On Windows:
     ```
     ./.venv/Scripts/activate
     ```
   - On Unix or MacOS:
     ```
     source venv/bin/activate
     ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

...existing code...

## Database Migrations

Run the following commands to apply database migrations:
```
python manage.py makemigrations
python manage.py migrate
```

...existing code...

## Running the App

Start the app by running:
```
python start.py
```

## If you have Docker installed
you just do docker-compose build
make sure you have .env file ready

      docker-compose up --build

...existing code...
