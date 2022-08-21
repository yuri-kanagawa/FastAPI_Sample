from typing import List
from typing import Type

from fastapi import status
from fastapi.responses import JSONResponse

common_error_cord = {
    200: {"response": "Successful Response"}, 
    400: {"response": "ParameterError"},
    401: {"response": "Unauthorized"},
    404: {"response": "Not Found"},
    422: {"response": "Validation Error"},
    500: {"response": "Internal Server Error"}
}

class ApiError(Exception):
    status_code: int = 400
    detail: str = 'Bad Request'

class Unauthorized(ApiError):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    detail: str = 'Unauthorized'

class DataNotFound(ApiError):
    status_code: int = status.HTTP_404_NOT_FOUND
    detail: str = 'Data Not Found'

class Conflict(ApiError):
    status_code: int = status.HTTP_409_CONFLICT
    detail: str = 'Conflict'

class Validation(ApiError):
    status_code: int = 422
    detail: str = 'Validation Error'

class InternalServer(ApiError):
    status_code: int = 500
    detail: str = 'Internal Server Error'

def error_response(error_types: List[Type[ApiError]]) -> dict:
    # error_types に列挙した ApiError を OpenAPI の書式で定義する
    d = {}
    for et in error_types:
        if not d.get(et.status_code):
            d[et.status_code] = {
                'description': f'{et.detail}',
                'content': {
                    'application/json': {
                        'example': {
                            'status_code': et.status_code,
                            'detail': {"type":et.detail,
                                        "msg": "DetailErrorMassage"}
                        }
                    }
                }}
        else:
            # 同じステータスコードなら description に追記
            d[et.status_code]['description'] += f'<br>{et.detail}'
    return d