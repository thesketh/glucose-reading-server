# glucose-reading-server

This is a submission I put together for a technical challenge to build a backend API to submit glucose readings for diabetic patients.

I built this as two separate packages:
 - A library which implements repositories for the data (using either a fake implementation using a Python dict, or SQLAlchemy)
 - A service (using FastAPI/uvicorn) which wraps the library with an API.

Both the store library and service use pydantic for validation of data models.

## Installation Instructions

Set up a new Python 3.8+ environment in the environment management tool of your choice (I like `miniforge`, but `pipenv`, `poetry` and
`virtualenv` are all popular). Clone the repo and `cd` into it.

There are a few options for using the code:

  1. Install the requirements with `pip` and run the code from where it is:
      - `pip install -r requirements.txt`
      - `cd` into the `src` folder: `cd src`
      - Check out the help menu for usage instructions with `python -m glucose_reading_server --help`
  2. Install the packages with setuptools:
      - `python setup.py install`
      - Check out the help menu for usage instructions with `glucose-reading-server --help`
  3. Install with development dependencies:
      - `pip install -e '.[dev]'`
      - Check out the help menu for usage instructions with `glucose-reading-server --help`


## Usage Instructions

These instructions assume you used option 2 or 3 above.

The API can be started in testing mode using a Python dict with the '-t' flag:
```
glucose-reading-server -t
```

which will not persist readings between the server being killed/restarted.

Alternatively, a SQLAlchemy connection string can be set at the command line or in an environment variable.
I used SQLite for testing:
```
glucose-reading-server -c "sqlite:///${HOME}/test_glucose_db.db"
```

## Testing Instructions

 - Run unit tests with `pytest`. This will require that you used option 3 above.
 - To run API tests:
    - Start the application.
    - Run the postman tests with `newman`:
      ```
      newman run postman-tests.json
      ```

      These have been modified slightly from the tests I was sent: the original tests expected status `404`
      for invalid UUIDs in the URL path, whereas this is considered a bad request (`400`) by this API. Valid
      UUIDs which are not in the system will correctly return a `404.`
