[This code's documentation lives on the grpc.io site.](https://grpc.io/docs/quickstart/python.html)

Generate gRPC Code
python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/ClientRequest.proto
