from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import exception_handler

def json_response(data=None, message=None, error=False, status_code=status.HTTP_200_OK):
    if error:
        response_data = {
            "success": False,
            "message": message or "An error occurred",
            "data": data or None
        }
        return Response(response_data, status=status_code)
    else:
        response_data = {
            "success": True,
            "message": message or "Request was successful",
            "data": data or None
        }
        return Response(response_data, status=status_code)
    
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code

    return response