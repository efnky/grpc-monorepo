import os

import grpc
from fastapi import FastAPI

import greeter_pb2
import greeter_pb2_grpc

app = FastAPI()

# Address of the greeter-server, e.g. "greeter-server:50051" (internal) or
# "greeter-server-xxxx.edge-1.komuta.app:443" (public). Set via env on deploy.
GREETER_ADDR = os.environ.get("GREETER_ADDR", "localhost:50051")
# Use TLS (needed when reaching the server through the public HTTPS ingress).
GREETER_TLS = os.environ.get("GREETER_TLS", "false").lower() == "true"


def _channel():
    if GREETER_TLS:
        return grpc.secure_channel(GREETER_ADDR, grpc.ssl_channel_credentials())
    return grpc.insecure_channel(GREETER_ADDR)


@app.get("/")
def call_grpc():
    info = {"grpc_addr": GREETER_ADDR, "tls": GREETER_TLS}
    try:
        with _channel() as channel:
            stub = greeter_pb2_grpc.GreeterStub(channel)
            reply = stub.SayHello(
                greeter_pb2.HelloRequest(name="komuta"), timeout=5
            )
        return {"ok": True, **info, "reply": reply.message}
    except grpc.RpcError as e:
        return {"ok": False, **info, "grpc_code": str(e.code()), "detail": e.details()}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, **info, "error": repr(e)}
