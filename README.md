# grpc-monorepo — two microservices in one repo (root-context)

Two services from one repository, to test komuta's multi-service-from-one-repo
deploy and **service-to-service gRPC**.

All source lives at the repo **root**; the two services differ only by which
**Dockerfile** is selected (build context is always the repo root, so there is
no per-service context to mis-assign):

- **Dockerfile.server** → `python server.py`, gRPC server on `:50051`.
- **Dockerfile.client** → `uvicorn app:app`, FastAPI HTTP + gRPC client on `:8000`.

Shared: `greeter.proto` + generated stubs (`greeter_pb2*.py`), union
`requirements.txt`.

## Deploy on komuta
Create **two services** from this one repo, both with build context = repo root,
differing by the **Configuration file**:
- service **server**: Configuration file = `Dockerfile.server` (port 50051)
- service **client**: Configuration file = `Dockerfile.client` (port 8000), env
  `GREETER_ADDR=<server-internal-addr>:50051`, `GREETER_TLS=false`

Deploy the server first, read its internal address, then point the client's
`GREETER_ADDR` at it. `GET /` on the client → `{"ok": true, "reply": "..."}`
means service-to-service gRPC worked.

## Local run
```bash
pip install -r requirements.txt
PORT=50051 python server.py &
GREETER_ADDR=localhost:50051 uvicorn app:app --port 8000
curl localhost:8000/
```
