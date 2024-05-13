# Notes

## Sqlalchemy

Some relevant sqlalchemy docs for the code we wrote:

[inserted_primary_key](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.inserted_primary_key)

`c.id`: `addresses_to_process.c.id` refers to the column id of the table addresses_to_process. The c stands for "column," and it's a way to access table columns in SQLAlchemy.

`scalar`: The method .scalar() returns the first element of the first result or None if there are no rows, making it a concise way to check for existence and fetch a simple value.


### Sessions

https://docs.sqlalchemy.org/en/20/orm/session_basics.html

#### When do you make a session?

As per sqlAlchemy docs:

> A Session is typically constructed at the beginning of a logical operation where database access is potentially anticipated.

#### Sessions per thread

As per sqlalchemy docs:

> When designing database applications for concurrency, the appropriate model is that each concurrent task / thread works with its own database transaction. This is why when discussing the issue of database concurrency, the standard terminology used is multiple, concurrent transactions. Within traditional RDMS there is no analogue for a single database transaction that is receiving and processing multiple commands concurrently.

> The concurrency model for SQLAlchemy’s Session and AsyncSession is therefore Session per thread, AsyncSession per task. An application that uses multiple threads, or multiple tasks in asyncio such as when using an API like asyncio.gather() would want to ensure that each thread has its own Session, each asyncio task has its own AsyncSession.

> The best way to ensure this use is by using the standard context manager pattern locally within the top level Python function that is inside the thread or task, which will ensure the lifespan of the Session or AsyncSession is maintained within a local scope.

#### Begin

Begin a transaction, or nested transaction, on this Session, if one is not already begun.

The Session object features autobegin behavior, so that normally it is not necessary to call the Session.begin() method explicitly. However, it may be used in order to control the scope of when the transactional state is begun.

When used to begin the outermost transaction, an error is raised if this Session is already inside of a transaction.


#### Add

Place an object into this Session.

Objects that are in the transient state when passed to the Session.add() method will move to the pending state, until the next flush, at which point they will move to the persistent state.

Objects that are in the detached state when passed to the Session.add() method will move to the persistent state directly.

If the transaction used by the Session is rolled back, objects which were transient when they were passed to Session.add() will be moved back to the transient state, and will no longer be present within this Session.

#### Commit

Session.commit() is used to commit the current transaction. At its core this indicates that it emits COMMIT on all current database connections that have a transaction in progress; from a DBAPI perspective this means the connection.commit() DBAPI method is invoked on each DBAPI connection.

When there is no transaction in place for the Session, indicating that no operations were invoked on this Session since the previous call to Session.commit(), the method will begin and commit an internal-only “logical” transaction, that does not normally affect the database unless pending flush changes were detected, but will still invoke event handlers and object expiration rules.

The Session.commit() operation unconditionally issues Session.flush() before emitting COMMIT on relevant database connections. If no pending changes are detected, then no SQL is emitted to the database. This behavior is not configurable and is not affected by the Session.autoflush parameter.

Subsequent to that, assuming the Session is bound to an Engine, Session.commit() will then COMMIT the actual database transaction that is in place, if one was started. After the commit, the Connection object associated with that transaction is closed, causing its underlying DBAPI connection to be released back to the connection pool associated with the Engine to which the Session is bound.

#### Sessionmaker

A configurable Session factory.

The sessionmaker factory generates new Session objects when called, creating them given the configurational arguments established here.


sessionmaker acts as a factory for Session objects in the same way as an Engine acts as a factory for Connection objects. In this way it also includes a sessionmaker.begin() method, that provides a context manager which both begins and commits a transaction, as well as closes out the Session when complete, rolling back the transaction if any errors occur:

```python3
Session = sessionmaker(engine)

with Session.begin() as session:
    session.add(some_object)
    session.add(some_other_object)
    # commits transaction, closes session
```

The class also includes a method sessionmaker.configure(), which can be used to specify additional keyword arguments to the factory, which will take effect for subsequent Session objects generated. This is usually used to associate one or more Engine objects with an existing sessionmaker factory before it is first used:

```python3
# application starts, sessionmaker does not have
# an engine bound yet
Session = sessionmaker()

# ... later, when an engine URL is read from a configuration
# file or other events allow the engine to be created
engine = create_engine('sqlite:///foo.db')
Session.configure(bind=engine)

sess = Session()
# work with session
```

#### Final thoughts on session

I think I can open one sesssion per thread but everywhere keeps saying use a `scoped_session`. Still unsure why tbh. Here are some quotes from the docs that support this idea:

> The Session is very much intended to be used in a non-concurrent fashion, which usually means in only one thread at a time.

> The Session should be used in such a way that one instance exists for a single series of operations within a single transaction. One expedient way to get this effect is by associating a Session with the current thread (see Contextual/Thread-local Sessions for background). Another is to use a pattern where the Session is passed between functions and is otherwise not shared with other threads.

and more on scoped_sessions

> The Session object is entirely designed to be used in a non-concurrent fashion, which in terms of multithreading means “only in one thread at a time”. So our above example of scoped_session usage, where the same Session object is maintained across multiple calls, suggests that some process needs to be in place such that multiple calls across many threads don’t actually get a handle to the same session. We call this notion thread local storage, which means, a special object is used that will maintain a distinct object per each application thread. Python provides this via the threading.local() construct. The scoped_session object by default uses this object as storage, so that a single Session is maintained for all who call upon the scoped_session registry, but only within the scope of a single thread. 

and 

> Using this technique, the scoped_session provides a quick and relatively simple (if one is familiar with thread-local storage) way of providing a single, global object in an application that is safe to be called upon from multiple threads.

## Errors during development

1. Non unique hashes.

Are hashes unique in etherscan? What is this happening?

```bash
IntegrityError: (psycopg2.errors.UniqueViolation) duplicate key value violates unique constraint "transactions_hash_key"
DETAIL:  Key (hash)=(0xc9c50c8d403dfe2545e467a2015d7b6311a9c26d3ab84c1985ec76de71efbfb7) already exists.
```

I think I understand what is happening. Wrote about this in [docs/notes_api.md](notes_api.md)

