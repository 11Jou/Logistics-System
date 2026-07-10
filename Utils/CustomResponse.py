from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class CustomResponse:
    RESPONSE_KEYS = ('success', 'message', 'data', 'error', 'status')

    @classmethod
    def build(cls, success, message='', data=None, error=None, status=200):
        return {
            'success': success,
            'message': message,
            'data': data,
            'error': error,
            'status': status,
        }

    @classmethod
    def is_formatted(cls, payload):
        return isinstance(payload, dict) and set(cls.RESPONSE_KEYS).issubset(payload.keys())

    @classmethod
    def success(cls, message='Success', data=None, status=200):
        return Response(
            cls.build(True, message=message, data=data, error=None, status=status),
            status=status,
        )

    @classmethod
    def error(cls, message='Error', error=None, status=400, data=None):
        return Response(
            cls.build(False, message=message, data=data, error=error, status=status),
            status=status,
        )


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get('response') if renderer_context else None

        if response is not None and not CustomResponse.is_formatted(data):
            status_code = response.status_code
            is_success = 200 <= status_code < 300
            data = CustomResponse.build(
                success=is_success,
                message='Success' if is_success else 'Request failed',
                data=data if is_success else None,
                error=None if is_success else data,
                status=status_code,
            )

        return super().render(data, accepted_media_type, renderer_context)


def custom_exception_handler(exc, context):
    from rest_framework.views import exception_handler

    response = exception_handler(exc, context)

    if response is None:
        return None

    error_detail = response.data
    message = 'Request failed'

    if isinstance(error_detail, dict):
        if 'detail' in error_detail:
            message = str(error_detail['detail'])
            error_detail = {'detail': error_detail['detail']}
        else:
            message = next(
                (str(value[0]) if isinstance(value, list) else str(value)
                 for value in error_detail.values()),
                message,
            )
    elif isinstance(error_detail, list):
        message = str(error_detail[0]) if error_detail else message
        error_detail = {'detail': error_detail}
    else:
        message = str(error_detail)
        error_detail = {'detail': error_detail}

    response.data = CustomResponse.build(
        success=False,
        message=message,
        data=None,
        error=error_detail,
        status=response.status_code,
    )
    return response
