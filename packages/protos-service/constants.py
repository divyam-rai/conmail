INPUT_FOLDER = "protos"
PROTOC_TARGET_FOLDER = "protoc-out"
DIST_FOLDER="dist"

PACKAGE_META = """
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "conprotos"
version = "0.0.1"
authors = [
  { name="Divyam Rai" },
]
description = "Protobuf definitions for the ConMail project."
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
  "protobuf"
]
"""