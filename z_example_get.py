import requests
from time import time

# # TODO: delete this file
# start = time()
# r = requests.get('http://127.0.0.1:8000/api/v1/it_works/', data={'code': 5})
# print(r.content)
# print('time taken:', time() - start)

# data = {"code": 'code',
#         "email": 'email',
#         "args": 'args',
#         "klee_args": "request.build_absolute_uri(reverse('jobs_notify'))",
#         "soft_time_limit": "worker_config.timeout"}
# task = requests.post('http://127.0.0.1:8000/api/v1/worker_submit_code/', data=data)
# print(task.content)

# source /src/worker/env/bin/activate

"""/src/worker_web ... something something  run python manage.py runserver

logs of worker and web: /src/worker/logs

running celery worker -A worker_web.worker.worker from within the src folder works! 
    so probably need to make sure that I run it from the right folder from the supervisor.
    
Now moved worker outside so need:
    celery worker -A worker_web.worker


"""

