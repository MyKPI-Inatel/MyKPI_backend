## Running Tests with Pytest

To run the tests, navigate to the `app` directory and execute the following command:

```bash
cd app
pytest
```

### Configuration

The `pytest.ini` file includes the following configuration to set up logging and markers:

```ini
[pytest]
log_cli=true
log_level=INFO
log_format = %(asctime)s %(levelname)s %(message)s
log_date_format = %Y-%m-%d %H:%M:%S

addopts = --strict-markers  
markers =
    dept: marks tests as department tests
    org: marks tests as organization tests
    quest: marks tests as question tests
    survey: marks tests as survey tests
    survquest: marks tests as surveyquestion test
    functional: marks tests as functional tests
    unit: marks tests as unit tests
```

- **log_cli**: Enables logging for the command line interface.
- **log_level**: Sets the logging level to `INFO`.
- **log_format**: Defines the format for log messages.
- **log_date_format**: Specifies the format for the timestamp in log messages.
- **addopts**: The `--strict-markers` option ensures that any markers used are defined in the configuration file.
- **markers**: Lists the custom markers available in the project, including:
  - `dept`: Marks tests as department tests.
  - `org`: Marks tests as organization tests.
  - `quest`: Marks tests as question tests.
  - `survey`: Marks tests as survey tests.
  - `survquest`: Marks tests as survey question tests.
  - `functional`: Marks tests as functional tests.
  - `unit`: Marks tests as unit tests.

### Environment Variables for Functional Tests

To run functional tests, ensure that the variables in your `.env.sh` file are properly configured. If these variables are not set, you can run only the unit tests using the following command:

```bash
pytest -m "unit"
```

### Running Specific Tests

You can also run tests with specific markers using the `-m` option. For example:

- To run tests marked as department tests, use:

  ```bash
  pytest -m "dept"
  ```

- To run tests marked as department tests that are not functional, use:

  ```bash
  pytest -m "dept and not functional"
  ```

- To run all tests except department tests, use:

  ```bash
  pytest -m "not dept"
  ```


### Generating Test Reports

By default, if no specific path is provided for the report, it will be generated at `test/cover/report.html`.

To specify a custom path for the report file, use the `--html` flag. Recommended paths include:

- For **unit tests**, use `test/cover/unit.html`:

  ```bash
  pytest -m "unit" --html=test/cover/unit.html
  ```

- For **functional tests**, use `test/cover/functional.html`:

  ```bash
  pytest -m "functional" --html=test/cover/functional.html
  ```

- For **all tests**, default to `test/cover/report.html`:

  ```bash
  pytest
  ```

This setup allows you to easily execute tests based on categories, providing flexibility in testing the application.