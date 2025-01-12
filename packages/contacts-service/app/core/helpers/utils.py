from flask import Response
from app.core.helpers.errors import ERROR_CODES
import json
import logging
import sys

def with_empty_attrib_as_null(value: str) -> str | None:
    if value == "":
        return None
    return value

def with_none_attrib_as_empty(value: str | None) -> str:
    if value == None:
        return ""
    return value

def get_logger(log_name: str):
    logger = logging.getLogger(log_name)

    # Setup JSON formatted logs sent to stdout.
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter("{'time':'%(asctime)s', 'name': '%(name)s', 'level': '%(levelname)s', 'message': '%(message)s'}")
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    return logger

def raise_error(key: str, data= {}, error= {}) -> Response:
    error_info = ERROR_CODES.get(key, ERROR_CODES["INTERNAL"])
    return response(error_info[0], error_info[1], data, error)

def response(status: int, data={}) -> Response:
    return Response(
        json.dumps(data),
        status= status,
        mimetype= 'application/json'
    )