# Blue Bite Back End Engineer Assignment

## Introduction
Vendors are sending us JSON payloads containing Tags and their Metadata.
This API is an attempt to store and retrieve those Tags. 

## JSON Schema
See bluebite/validation/schema.json, and tests/json_payloads/

## Functionality
1. Accept JSON Payloads via HTTP RESTful routes
    - Validate incoming commands
    - Parse Payload and store data appropriately
2. Query by metadata interface
    - Validate incoming queries
    - Return all tags including the queried metadata

## Deliveables
- Python
- Any framework, tools, or libraries so long as they're open source and publically available
- Any relationhal datastore, so long as it is available on macOS or Linux
- Submit assignment to a version control repository accessible to Blue Bite

## Setup
It's recommended that you set up and activate a new virtualenvironment before running this application.
See https://virtualenv.pypa.io/en/stable/ for more details.
Please ensure that you have Postgresql installed.

### macOS
```bash
$ brew install postgresql
$ brew services start postgresql # if you want postgresql to start up at login
```

### Linux (Debian)
```bash
$ sudo apt-get install postgresql-9.4 postgresql-client-9.4
```

Once Postgres is running and you've activated your virtual environment you can simply execute
```bash
$ ./bin/setup-and-run
```
and the smart tag API will be up and running on localhost:5000

## Test
Inside your virtualenvironment run the following.
```bash
$ pip install -r tests/requirements.txt
$ pytest
```

## Notes
- The way the API is currently implemented is not efficient for large payloads. If I had more foresight and time I would implement an asynchronous workflow to handle saving Tags and Meta data to the database. I think a Celery and Rabbit solution would work nicely.
- I opted to use custom Postgresql connection and session management rather than Flask-SQLAlchemy. I did this because it's more familiar to me. 
