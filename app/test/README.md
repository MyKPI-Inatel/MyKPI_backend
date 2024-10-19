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
    functional: marks tests as functional tests
```

- **log_cli**: Enables logging for the command line interface.
- **log_level**: Sets the logging level to `INFO`.
- **log_format**: Defines the format for log messages.
- **log_date_format**: Specifies the format for the timestamp in log messages.
- **addopts**: The `--strict-markers` option ensures that any markers used are defined in the configuration file.
- **markers**: Lists the custom markers available in the project, including:
  - `dept`: Marks tests as department tests.
  - `org`: Marks tests as organization tests.
  - `functional`: Marks tests as functional tests.

### Environment Variables for Functional Tests

To run functional tests, ensure that the variables in your `.env.sh` file are properly configured. If these variables are not set, you can run only the non-functional tests using the following command:

```bash
pytest -m "not functional"
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

This setup makes it easy to execute tests and organize them based on categories, providing flexibility in testing your application.