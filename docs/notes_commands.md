# Notes

These notes are mostly for me to just remember how to use the tools lol. 

## Docker commands

To get inside postgres container, first get the container id:

```bash
docker ps
```

Then:

```bash
docker exec -it <container id> psql -U postgres
```

To kill a container:

```bash
docker kill <container_id>
```

## Postgresql commands

To see all tables:

```postgresql
\dt
```
We have 2 tables `addresses` and `transactions`

you can get the count of a table during ingestion:

```postgresql
select count(1) from transactions;
```

```postgresql
select count(1) from addresses;
```

Drop tables if needed:

```psql
drop table transactions cascade; drop table addresses cascade
```


## Poetry

To add a dev-dependency

```bash
poetry add <dev dependency> -G dev
```

## Pytest

To run a specific test:

```bash
poetry run pytest -vv -s tests/unit/test_ingest.py::TestIngest::test_ingest_simple_result_less_than_10k
```
