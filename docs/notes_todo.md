# Notes

This is my todo list for this project. I have some Todos for mvp2.

## Todo list for the backend

- [x] determine data model for transasctions
- [x] handle IntegrityError
- [x] use `scoped_session`
- [x] normalize tables for addresses
- [x] look up how to use logger and logging levels
- [x] handle errors for batch inserts
- [x] use orm sqlalchemy for more class declarative models
- [x] play with api. note the gotchas, notably how to get all addresses despite the 10k limit. probably have to thread a large start/end block and then within each thread, divide each section into 10k batches. ugh.
- [x] consider architecture. next.js with server side rendering only or do we need a server? Do we actually need a server or is it simpler with just next.js and server side rendering. We probably want caching and pagination. Can next.js do this alone?
- [x] index transactions on timestamp since that's how we'll query the data.
- [x] index addresses on address
- [x] implement a way to only work with a small window of records at a time during testing. maybe start with a small window using startBLock and a small endBlock
- [x] store timestamps in utc you moron.
- [x] modularize the ingest file. too big. so many concerns.
- [x] mock out the ingestor to test the crawl and ingest command
- [x] mock out the threadcontextmanager in the crawl and ingest test
- [ ] write integration test, end to end starting with the click/typer command. and then inspecting the state of the database. I guess you still have to mockout the etherscan request here.
- [ ] build a matlibplot or some pandas just because.
- [ ] implement crawling for more addresses to query. create a queue (a table is fine maybe with `queued` and `visited` columns) for all the from_addresses and to_addresses you see. Sort of like web crawling.
- [ ] my divide and conquer approach is inefficient because some block windows are hot spots whereas others are not. You can actually see this in the frontend aggregated view! There are some days with much larger amounts of transactions than others so... some Threads finish super quickly while others take too long. We should constantly be dividing and conquering the block windows. That's MVP2.
- [ ] build a way to provide a timestamp and ingest records after that timestamp (this would be great for an orchestrator like Airflow)


## Todo for frontend
- [x] build out prototype with next.js
- [x] consider if you actually need a backend? server side rendering should be enough?
- [x] I think we should filter by account. So adjust queries and have a place to type in accounts
- [x] be able to filter by date. A calendar?
- [x] css and styling... badly needed.
- [x] fix  timestamp bug. write a test to check that timestamp in database the same as timestamp on page.
- [x] display the address that we're focusing on in the header
- [ ] some graphical libraries. chart.js?
- [ ] caching in the server using redis, cache on address and datetime/timestamp. invalidate cache when it holds too many records FIFO style.
- [ ] you need to write some frontend tests that involve interaction. Setup a test db and then click around the web


## Todo General
- [ ] docker compose everything.
