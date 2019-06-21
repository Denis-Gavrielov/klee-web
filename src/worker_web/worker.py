import os
import subprocess
import re
import sys  # TODO: delete

from celery import Celery
from celery.worker.control import Panel
from celery.exceptions import SoftTimeLimitExceeded
from billiard import current_process

from runner import WorkerRunner
from worker_config import WorkerConfig


celery = Celery(broker=os.environ['CELERY_BROKER_URL'], backend='rpc')

worker_config = WorkerConfig()


@Panel.register
def get_uptime_stats(state):
    uptime_pattern = re.compile(
        r'up\s+(.*?),\s+([0-9]+) '
        r'users?,\s+load averages?: '
        r'([0-9]+\.[0-9][0-9]),?\s+([0-9]+\.[0-9][0-9])'
        r',?\s+([0-9]+\.[0-9][0-9])')

    uptime_output = subprocess.check_output('uptime')
    uptime_matches = uptime_pattern.search(uptime_output)

    return {
        'uptime': uptime_matches.group(1),
        'users': uptime_matches.group(2),
        'loadavg_1min': uptime_matches.group(3),
        'loadavg_5min': uptime_matches.group(4),
        'loadavg_15min': uptime_matches.group(5),
    }


@celery.task(name='submit_code', bind=True)
def submit_code(self, code, email, klee_args, endpoint):
    print('\nMADE IT THIS FAR', file=sys.stderr)
    # name will hold the name of the current worker, which is in the format
    # celery@name, so we split at @ and take the second part
    name = current_process().initargs[1].split('@')[1]
    print('\nMADE IT THIS FAR 2', file=sys.stderr)
    print('REQUEST ID:', self.request.id)
    print('ENDPOINT:', endpoint)
    with WorkerRunner(self.request.id, endpoint, worker_name=name) as runner:
        print('\nMADE IT THIS FAR 3', file=sys.stderr)
        try:
            print('\nMADE IT THIS FAR 4', file=sys.stderr)
            print('BEFORE RUNNER RUN, KLEE_ARGS:', klee_args)
            runner.run(code, email, klee_args)
            print('\nMADE IT THIS FAR 5', file=sys.stderr)
        except SoftTimeLimitExceeded:
            print('\nMADE IT THIS FAR 6', file=sys.stderr)
            result = {
                'klee_run': {
                    'output': 'Job exceeded time limit of '
                              '{} seconds'.format(worker_config.timeout)
                }
            }
            print('\nMADE IT THIS FAR 7', file=sys.stderr)
            runner.send_notification('job_failed', result)
            print('\nMADE IT THIS FAR 8', file=sys.stderr)
