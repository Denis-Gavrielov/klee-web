# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

# from worker.worker import submit_code

@api_view()
def it_works(request):
    """Test that the requests work well."""
    print(request.data)
    print(request.method)
    return Response({'this works': 'too'})


@api_view(['POST'])
def worker_submit_code(request):
    # code = request.data.get("code")
    # email = request.data.get("email")
    # args = request.data.get("args")
    # klee_args = request.data.get("klee_args")
    # soft_time_limit = request.data.get("soft_time_limit")

    # TODO: import submit_code function from worker
    # task = submit_code.apply_async(code, email, args, klee_args, soft_time_limit)
    return Response(request.data)

