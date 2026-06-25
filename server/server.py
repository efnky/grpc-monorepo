import os
from concurrent import futures

import grpc

import greeter_pb2
import greeter_pb2_grpc


class Greeter(greeter_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        # This method runs on the server when a client calls SayHello.
        return greeter_pb2.HelloReply(
            message=f"Hello, {request.name}! (reply from greeter-server)"
        )


def serve():
    port = os.environ.get("PORT", "50051")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    greeter_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port(f"0.0.0.0:{port}")
    server.start()
    print(f"greeter-server (gRPC) listening on 0.0.0.0:{port}", flush=True)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
