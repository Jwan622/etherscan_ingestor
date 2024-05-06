# Notes


## Dirty QA

1. Run it twice, see if the counts are the same. I'm looking an abbreviated window for this address:

```bash
postgres=# select count(1) from addresses;
 count
-------
  6283
(1 row)

postgres=# select count(1) from transactions;
 count
-------
 25032
(1 row)

postgres=# drop table addresses cascade;
NOTICE:  drop cascades to 2 other objects
DETAIL:  drop cascades to constraint transactions_from_address_id_fkey on table transactions
drop cascades to constraint transactions_to_address_id_fkey on table transactions
DROP TABLE
postgres=# drop table transactions cascade;
DROP TABLE
postgres=# select count(1) from transactions;
 count
-------
 25032
(1 row)

postgres=# select count(1) from addresses;
 count
-------
  6283
(1 row)
```

Looks good for the dirty QA of setting a small block_number of records to ingest, running it once, dropping all transactions, running again, check if the records match.

other queries look sane:

```bash
postgres=# select count(1) from addresses;
 count
-------
  6283
(1 row)

postgres=# select count(distinct address) from addresses;
 count
-------
  6283
(1 row)
```

## QA with a larger amount or records

