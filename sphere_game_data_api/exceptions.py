from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides better error responses
    instead of 500 Internal Server Error
    """
    
    # Get the standard error response first
    response = exception_handler(exc, context)
    
    if response is not None:
        # Log the error for debugging
        logger.error(f"API Error: {exc} - Context: {context}")
        
        # Customize error response format
        custom_response_data = {
            'error': True,
            'status_code': response.status_code,
            'message': 'An error occurred',
            'details': response.data
        }
        
        # Handle specific error types
        if isinstance(exc, ValidationError):
            custom_response_data['message'] = 'Validation error'
            custom_response_data['status_code'] = status.HTTP_400_BAD_REQUEST
            
        elif isinstance(exc, IntegrityError):
            custom_response_data['message'] = 'Database integrity error'
            custom_response_data['status_code'] = status.HTTP_400_BAD_REQUEST
            
        # Handle specific HTTP status codes
        if response.status_code == 400:
            custom_response_data['message'] = 'Bad Request - Please check your input data'
        elif response.status_code == 401:
            custom_response_data['message'] = 'Authentication required'
        elif response.status_code == 403:
            custom_response_data['message'] = 'Permission denied'
        elif response.status_code == 404:
            custom_response_data['message'] = 'Resource not found'
        elif response.status_code == 405:
            custom_response_data['message'] = 'Method not allowed'
        elif response.status_code == 429:
            custom_response_data['message'] = 'Too many requests'
            
        response.data = custom_response_data
        
    else:
        # Handle unhandled exceptions (500 errors)
        logger.error(f"Unhandled Exception: {exc} - Context: {context}")
        
        # Create a proper error response
        response = Response(
            {
                'error': True,
                'status_code': 500,
                'message': 'Internal server error occurred',
                'details': str(exc) if hasattr(exc, '__str__') else 'Unknown error'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return response
