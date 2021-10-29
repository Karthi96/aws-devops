import sys
import traceback
import time

from src.register.constant import HttpRequestParamType, generate_lambda_response, make_response_body
from src.register.exceptions import InternalServerErrorException


def exception_handler(*decorator_args, **decorator_kwargs):
    logger = decorator_kwargs["logger"]

    def decorator(func):
        EXCEPTIONS = decorator_kwargs.get("EXCEPTIONS", ())

        def get_exec_info():
            exec_info = sys.exc_info()
            formatted_exec_info = traceback.format_exception(*exec_info)
            exception_info = ""
            for exc_lines in formatted_exec_info:
                exception_info = exception_info + exc_lines
            return exception_info

        def wrapper(*args, **kwargs):
            event = kwargs.get("event", args[0])
            now = time.time()

            handler_name = decorator_kwargs.get("handler_name", func.__name__)
            path = event.get("path", None)
            headers = event.get(HttpRequestParamType.REQUEST_HEADER.value, {})
            path_parameters = event.get(HttpRequestParamType.REQUEST_PARAM_PATH.value, {})
            query_string_parameters = event.get(HttpRequestParamType.REQUEST_PARAM_QUERY_STRING.value, {})
            body = event.get(HttpRequestParamType.REQUEST_BODY.value, "{}")

            error_message = f"Error Reported! \n" \
                            f"path: {path}, \n" \
                            f"handler: {handler_name} \n" \
                            f"header: {headers} \n" \
                            f"pathParameters: {path_parameters} \n" \
                            f"queryStringParameters: {query_string_parameters} \n" \
                            f"body: {body} \n" \
                            f"error_description: \n"

            try:
                func_response = func(*args, **kwargs)
                later = time.time()
                difference = int(later - now)

                print(f"Time taken for handler name = {handler_name} time={difference} seconds")
                return func_response
            except EXCEPTIONS as e:
                exec_info = get_exec_info()
                logger.exception(error_message + exec_info)
                return generate_lambda_response(
                    e.status_code,
                    make_response_body("", e.error_message))
            except:
                exec_info = get_exec_info()
                logger.exception(error_message + exec_info)
                return generate_lambda_response(
                    InternalServerErrorException().status_code,
                    make_response_body("", InternalServerErrorException().error_message))

        return wrapper

    return decorator
