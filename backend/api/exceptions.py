"""
Custom exception handler for API.
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides consistent error responses.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Customize the response format
        custom_response_data = {
            'success': False,
            'error': {
                'message': str(exc),
                'code': response.status_code,
                'details': response.data
            }
        }
        response.data = custom_response_data

    # Log the exception
    logger.error(f"API Exception: {exc}", exc_info=True)

    return response
