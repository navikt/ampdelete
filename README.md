# ampdelete

Delete amplitude IDs from the command line!

### Prerequisites

- [Poetry](https://python-poetry.org/docs/#installation)

After installation, run the following command to create the environment for the application:

```bash
poetry install
```

### secret.py

Create a file named `secret.py` inside the `src` directory.
This file must contain the API key and secret key for the project you wish to run deletions on, and is required to run the command-line interface.

The file contents of `secret.py` should look like this, replacing the values as you see fit.

```
API_KEY="your api key here"
SECRET_KEY="your secret key here"
```

### Running

This assumes that the CSV is well-formed, and that there exists a key named "amplitude_id" (without any tabs inside the string, and so on).

```bash
poetry run python delete path/to/csv-file.csv
```