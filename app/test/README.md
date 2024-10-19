## Running Tests with Pytest

To run the tests, simply navigate to the `app` directory and execute the following command:

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
```

- **log_cli**: Enables logging for the command line interface.
- **log_level**: Sets the logging level to `INFO`.
- **log_format**: Defines the format for log messages.
- **log_date_format**: Specifies the format for the timestamp in log messages.
- **addopts**: The `--strict-markers` option ensures that any markers used are defined in the configuration file.
- **markers**: Lists the custom markers available in the project.

You can also run tests with specific markers using the `-m` option. For example, to run tests marked as department tests, use:

```bash
pytest -m "dept"
```

Or, to run all tests except department tests, use:

```bash
pytest -m "not dept"
```

This setup makes it easy to execute tests and organize them based on categories, providing flexibility in testing your application.