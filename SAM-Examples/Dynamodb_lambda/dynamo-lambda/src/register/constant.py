import enum
import json


class HttpRequestParamType(enum.Enum):
    REQUEST_PARAM_QUERY_STRING = 'queryStringParameters'
    REQUEST_PARAM_PATH = 'pathParameters'
    REQUEST_BODY = 'body'
    REQUEST_HEADER = 'headers'
    REQUEST_PARAM_MULTI_VALUE_QUERY_STRING = 'multiValueQueryStringParameters'
    REQUEST_CONTEXT = 'requestContext'


def generate_lambda_response(status_code, message, headers=None, cors_enabled=True):
    response = {
        'statusCode': status_code,
        'body': json.dumps(message),
        'headers': {'Content-Type': 'application/json'}
    }
    if cors_enabled:
        response["headers"].update({
            "X-Requested-With": '*',
            "Access-Control-Allow-Headers": 'Access-Control-Allow-Origin, Content-Type, X-Amz-Date, Authorization,'
                                            'X-Api-Key,x-requested-with',
            "Access-Control-Allow-Origin": '*',
            "Access-Control-Allow-Methods": 'GET,OPTIONS,POST'
        })
    if headers is not None:
        response["headers"].update(headers)
    return response

def make_response_body(data, error):
    return {
        "data": data,
        "error": error
    }