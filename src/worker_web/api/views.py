# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

# from worker.worker import submit_code, celery
# from worker.worker_config import WorkerConfig

@api_view()
def it_works(request):
    """Test that the requests work well."""
    print(request.data)
    print(request.method)
    return Response({'this works': 'too'})


@api_view(['POST'])
def worker_submit_code(request):
    """
    Call the submit_code celery function asynchronously.

    TODO: here we are calling an asynchronous function. Check if that will
    still be asynchronous given the new pipeline.
    """
    code = request.data.get("code")
    email = request.data.get("email")
    args = request.data.get("args")
    klee_args = request.data.get("klee_args")
    soft_time_limit = request.data.get("soft_time_limit")

    # TODO: import submit_code function from worker
    task = submit_code.apply_async(code, email, args, klee_args, soft_time_limit)
    return Response(request.data)

@api_view()
def worker_config_timeout(request):
    """
    Get the current timeout for the redis queue in the klee_worker namespace.
    """
    worker_configuration = WorkerConfig()
    return Response(worker_configuration.timeout)

