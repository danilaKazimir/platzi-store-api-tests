## Local Checks And Tests Run

Run linting, formatting checks, type checking, and tests:

```bash
make check
```

Automatically fix linting and formatting issues:

```bash
make format
```

Run tests:

```bash
make test
```

## Logging

Test execution logs are written to the `logs` directory. Because the test suite
runs in parallel with `pytest-xdist`, each worker writes to a separate file:

```text
logs/pytest_2026-07-17_18-46-11_gw0.log
logs/pytest_2026-07-17_18-46-11_gw1.log
```

HTTP request and response logs include the method, URL, status code, and body.
Sensitive fields such as passwords and tokens are masked. Both successful and
failed HTTP responses are logged.

The `logs` directory is generated locally and is not committed to Git.

## Allure Reports

Running `make test` writes Allure test results to the `allure-results`
directory. The directory is cleaned before each test run.

To open an interactive report after the tests finish, install the Allure CLI
and run:

```bash
allure serve allure-results
```

To generate a static report instead, run:

```bash
allure generate allure-results --clean -o allure-report
allure open allure-report
```

The `allure-results` and `allure-report` directories are generated locally and
are not committed to Git.

## Running Tests in Docker

Build the Docker image:

```bash
docker build -t platzi-store-api-tests .
```

Run the tests using configuration from the local `.env` file:

```bash
docker run --rm --env-file .env platzi-store-api-tests
```
