from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

# from worker.worker import celery


@api_view()
def it_works(request):
    """Test that the requests work well."""
    print(request.data)
    print(request.method)
    return Response({'this works': 'too'})