# Notes

## Sqlalchemy

Some relevant sqlalchemy docs for the code we wrote:

[inserted_primary_key](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.inserted_primary_key)

`c.id`: `addresses_to_process.c.id` refers to the column id of the table addresses_to_process. The c stands for "column," and it's a way to access table columns in SQLAlchemy.

`scalar`: The method .scalar() returns the first element of the first result or None if there are no rows, making it a concise way to check for existence and fetch a simple value.


## Errors during development

1. Non unique hashes.

Are hashes unique in etherscan? What is this happening?

```bash
IntegrityError: (psycopg2.errors.UniqueViolation) duplicate key value violates unique constraint "transactions_hash_key"
DETAIL:  Key (hash)=(0xc9c50c8d403dfe2545e467a2015d7b6311a9c26d3ab84c1985ec76de71efbfb7) already exists.
```

I think I understand what is happening. Wrote about this in [docs/notes_api.md](notes_api.md)

