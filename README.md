# grpc-monorepo — two microservices in one repo

Two services in a single repository, to test whether komuta can deploy **multiple
microservices from one repo** and let them talk to each other over **gRPC**.

```
server/   gRPC server (Greeter.SayHello), listens on :50051   — its own Dockerfile
client/   FastAPI HTTP service + gRPC client                   — its own Dockerfile
```

- **server/** — pure gRPC server (HTTP/2). `GET` it over HTTP won't work; it's
  reached by the client over gRPC.
- **client/** — `GET /` calls the server's `SayHello` over gRPC and returns the
  reply as JSON. Target address from env `GREETER_ADDR` (+ `GREETER_TLS`).

Each subdirectory is a self-contained service with its own `Dockerfile`, so on
komuta you create **two services from this one repo**, each rooted at its
subdirectory (`server/` and `client/`).

## The question this probes
Two **separately-deployed** repos could not reach each other (no internal DNS;
public edge 403s gRPC). Do two services that live in the **same repo / project**
get internal connectivity so the client can reach the server over gRPC?

## How to deploy
1. Create service **server** from this repo, root path `server/`. Note its
   address (internal hostname if shown).
2. Create service **client** from this repo, root path `client/`. Set
   `GREETER_ADDR` to the server's address (e.g. `<server-internal>:50051`,
   `GREETER_TLS=false`).
3. Open the client URL → `{"ok": true, "reply": "..."}` means gRPC worked.

## Local run
```bash
# terminal 1
cd server && pip install -r requirements.txt && PORT=50051 python server.py
# terminal 2
cd client && pip install -r requirements.txt && GREETER_ADDR=localhost:50051 uvicorn app:app --port 8000
curl localhost:8000/
```
