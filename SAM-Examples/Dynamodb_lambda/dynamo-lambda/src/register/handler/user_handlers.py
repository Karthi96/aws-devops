import json
from http import HTTPStatus

from src.register.constant import make_response_body, generate_lambda_response
from src.register.exception_handler import exception_handler
from src.register.exceptions import EXCEPTIONS, BadRequestException
from src.register.logger import get_logger
from src.register.service.user_service import UserService

logger = get_logger(__name__)
user_service = UserService()


@exception_handler(logger=logger, EXCEPTIONS=EXCEPTIONS)
def create_user_handler(event, context):
    body = json.loads(event.get("body", {}))

    if body.get("email_id") is None:
        raise BadRequestException()

    response = user_service.create_user(user_payload=body)
    return generate_lambda_response(HTTPStatus.OK.value, make_response_body(response, ""))


@exception_handler(logger=logger, EXCEPTIONS=EXCEPTIONS)
def user_login_handler(event, context):
    body = json.loads(event.get("body", {}))

    if body.get("user_name") is None:
        raise BadRequestException()

    response = user_service.user_login(username=body.get("user_name"))
    return generate_lambda_response(HTTPStatus.OK.value, make_response_body(response, ""))


@exception_handler(logger=logger, EXCEPTIONS=EXCEPTIONS)
def write_data_handler(event, context):
    headers = event.get("headers", {})
    body = json.loads(event.get("body", {}))

    token = headers.get("token")

    if token is None or body is None:
        raise BadRequestException()

    response = user_service.write_data(token=token, payload=body)
    return generate_lambda_response(HTTPStatus.OK.value, make_response_body(response, ""))



