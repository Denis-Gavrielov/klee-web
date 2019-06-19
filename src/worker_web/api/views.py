# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

# from worker.worker import submit_code, celery
# from worker.worker_config import WorkerConfig
from .klee_tasks import *

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
    return Response(task)

@api_view()
def worker_config_timeout(request):
    """
    Get the current timeout for the redis queue in the klee_worker namespace.
    """
    worker_configuration = WorkerConfig()
    return Response(worker_configuration.timeout)@api_view()


@api_view()
def worker_config_cpu_share(request):
    """
    Get the current cpu share for the redis queue in the klee_worker namespace.
    """
    worker_configuration = WorkerConfig()
    return Response(worker_configuration.cpu_share)


@api_view()
def worker_config_memory_limit(request):
    """
    Get the current memory limit for the redis queue in the klee_worker namespace.
    """
    worker_configuration = WorkerConfig()
    return Response(worker_configuration.memory_limit)


@api_view(['POST'])
def worker_config_set_config(request):
    """
    Set configuration of worker.
    """
    # TODO: possibly have one WorkerConfig at top of this file
    worker_configuration = WorkerConfig()
    conf = request.data.get('conf')
    data = request.data.get('data')
    return Response(worker_configuration.set_config(conf, data))


@api_view()
def celery_get_workers(request):
    """
    Get celery workers.
    """
    return Response(get_workers())


@api_view()
def celery_registered_tasks(request):
    """
    Get the registered tasks of the worker.
    """
    workers = request.data.get('workers')
    return Response(registered_tasks(workers))


@api_view()
def celery_active_tasks(request):
    """
    Get the currently executing tasks from worker.
    """
    workers = request.data.get('workers')
    return Response(active_tasks(workers))


@api_view()
def celery_scheduled_tasks(request):
    """
    Get the scheduled tasks from worker
    """
    workers = request.data.get('workers')
    return Response(scheduled_tasks(workers))


@api_view()
def celery_active_queues(request):
    """
    Get the active queues from worker.
    """
    workers = request.data.get('workers')
    return Response(active_queues(workers))


@api_view()
def celery_reserved_tasks(request):
    """
    Returns tasks taken off the queue by a worker, waiting to be executed.
    """
    workers = request.data.get('workers')
    return Response(reserved_tasks(workers))


@api_view()
def celery_revoked_tasks(request):
    """
    Returns the tasks that have been revoked by workers.
    """
    workers = request.data.get('workers')
    return Response(revoked_tasks(workers))


@api_view()
def celery_control_broadcast(request):
    """
    Broadcast a control to celery workers
    """
    broadcast_return = celery.control.broadcast(request.data)
    return Response(broadcast_return)


