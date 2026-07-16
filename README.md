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

## Running Tests in Docker

Build the Docker image:

```bash
docker build -t platzi-store-api-tests .
```

Run the tests using configuration from the local `.env` file:

```bash
docker run --rm --env-file .env platzi-store-api-tests
```
