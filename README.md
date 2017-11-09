This is the code for the project for distributed computing.
please upload the code to the src folder.

Generate gRPC Code
python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/ClientRequest.proto
