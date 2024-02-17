# PyAsync Server

An async server realization using `asyncio` in python.

## Code Structure

- server.py: High-performance async server codes.
- client.py: High-performance async client codes.
- package.py: Define the format of different packages and ways to parse them.
- actions.py: Main logic of actions to process after received packages.
- protocol.py: Define how to frame a package.
- utils.py: Common utils defines here.

## Adding a New Action

Adding a new action in `pyasync_server` could be no more easier with following steps:

1. Define a function in `actions.py`.

   The arguments reveal data you need when executing the action. Paying attention to them is quite useful when defining the package structure later.

2. Add new package type in `package.py`.

   `package` is the minimum unit where data is stored of each request. To define a new package type, you should:

   1. Add new enumeration to the class `PACKAGE`.

   2. Define functions to pack your new packages.

      For example, `REQUEST_MARIADB_TEST` and `ANSWER_MARIADB_TEST`.

3. Add a new flow in `unpack_and_process()` in `actions.py`

## Client User Guide

You probably need following functions in `common.utils` before using the client:

- `handle_run_main()`: Run the main function in cli environment with simple error handling and logging.
- `resolve_client_ssl_context()`: Resolve the SSL context for client connection. (Optional)

## TLS Support

TLS is disabled by default. To enable it, follow the instructions below:

Use this command to generate keys and certification annually:

```bash
openssl req -newkey rsa:2048 -nodes -keyout server.key -x509 -days 365 -out server.crt -batch
```

- -x509: to generate self-signed certification
- -days: period of validity
- -nodes: don't encrypt the private key
- -batch: use default of configured settings instead of getting them interactively

Make sure your client and server use the same `server.crt`.

DO NOT DISTRIBUTE YOUR `server.key`!!!

At last, modify `enable_tls` to `True` in `config.py`.

Now your connections are under the protection of TLS.

## Database Support

Database is disabled by default. To enable it, follow the instructions below:

Edit `requirements.txt` to enable modules related to database you need and install them with:

```bash
pip install -r requirements.txt
```

Edit `server_config.py` to set parameters for connecting the database.

Finally, use `connect()` to visit your database and do what you want.

## TODOs

1. Compression threshold
2. MQ and Cluster support
