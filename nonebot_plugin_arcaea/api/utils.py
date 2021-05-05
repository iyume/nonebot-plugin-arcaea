from httpx import Response

from .exceptions import HTTPException


def http_status_handler(response: Response) -> None:
    status_code = response.status_code
    if status_code == 200:
        return
    exception = HTTPException(
        status_code=status_code, detail={
            400: 'Bad request',
            403: 'Forbidden',
            404: 'Page not found',
            422: 'Validation error'
        }.get(status_code)
    )
    raise exception
