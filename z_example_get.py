import requests
from time import time

# TODO: delete this file
start = time()
r = requests.get('http://127.0.0.1:8000/api/v1/it_works/', data={'code': 5})
print(r.content)
print('time taken:', time() - start)

# data = {"code": 'code',
#         "email": 'email',
#         "args": 'args',
#         "klee_args": "request.build_absolute_uri(reverse('jobs_notify'))",
#         "soft_time_limit": "worker_config.timeout"}
# task = requests.post('http://127.0.0.1:8000/api/v1/worker_submit_code/', data=data)
# print(task.content)