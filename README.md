# PyAsync Server

An async server realization using `asyncio` in python.

## Code Structure

- server.py
- client.py
- protocol.py
- utils.py
- benchmark.py
- compresser_benchmark.py

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

## TODOs

1. Compression threshold
2. Compression benchmark
