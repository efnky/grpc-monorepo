# grpc-monorepo — two microservices in one repo

Two services from one repository, to test komuta's multi-service-from-one-repo
deploy and **service-to-service gRPC**.

```
server/   Dockerfile -> python server.py   (gRPC server, :50051)
client/   Dockerfile -> uvicorn app:app     (FastAPI HTTP + gRPC client, :8000)
```

komuta detects one service per subdirectory that contains a file named exactly
`Dockerfile`. The two subdirectories differ only in their `Dockerfile`
(CMD/EXPOSE).

## Note on the layout (platform workaround)
komuta's monorepo scanner mis-assigns the build **context** of the second
service to `./client`. To stay robust against that, **both subdirectories carry
the full source** (`server.py` + `app.py` + stubs). So whichever context the
platform picks, the needed entrypoint file is present and the service builds.

## Deploy
Two services from this repo:
- **server** → `server/Dockerfile`, port 50051 (pure gRPC; its public HTTP URL
  will 502 — that's expected; reach it from the client over gRPC).
- **client** → `client/Dockerfile`, port 8000, env
  `GREETER_ADDR=<server-internal-addr>:50051`, `GREETER_TLS=false`.

Deploy server first, read its internal address, point the client's
`GREETER_ADDR` at it. `GET /` on the client → `{"ok": true, "reply": "..."}`
means service-to-service gRPC worked.

## Local run
```bash
cd server && pip install -r requirements.txt && PORT=50051 python server.py &
cd client && pip install -r requirements.txt && GREETER_ADDR=localhost:50051 uvicorn app:app --port 8000
curl localhost:8000/
```
