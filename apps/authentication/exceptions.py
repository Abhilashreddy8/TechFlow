from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler — ensures ALL errors return clean JSON.
    In a real company API, clients (mobile app, frontend) expect JSON always.
    HTML error pages break their apps.
    """

    # First call DRF's default handler
    # It handles most common errors like 400, 401, 403, 404
    response = exception_handler(exc, context)

    if response is not None:
        # DRF handled it — we just reformat the response to be cleaner
        error_data = {
            "success": False,
            "status_code": response.status_code,
            "errors": response.data
            # response.data contains the actual error details
        }
        response.data = error_data
        return response

    # DRF did NOT handle it — this means it's an unexpected server error
    # We catch it here so it never returns an ugly HTML crash page
    return Response({
        "success": False,
        "status_code": 500,
        "errors": {
            "detail": "Something went wrong. Our team has been notified."
            # Never expose real error details in production
            # Internal errors should be logged, not shown to users
        }
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)