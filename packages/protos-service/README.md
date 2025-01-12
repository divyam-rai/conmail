# Protos Service

This service hosts and serves the protobuf definitions required by the project. The output of this service is a package that can be installed by other services to get python definitions of the protobuf messages.

To build the package:
`python main.py`

To install the package from other services:
`pip install <path to .whl file>`