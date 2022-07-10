from time import sleep
from typing import List

from deepsource.celery_app import app
from deepsource.util.file_operations import gather_file_paths

import multiprocessing
import sys


def start_scanning(paths: List[str] = None) -> list:
    from deepsource.tasks.scan_file import scan_file
    task_ids = []
    for path in paths:
        task_id = scan_file.delay(path)
        task_ids.append(task_id)
    return task_ids


def start_worker():
    from deepsource.tasks import scan_file

    app.register_task(scan_file)

    worker = app.Worker(app=app, quiet=True)
    worker.start()


def deepsource():
    valid_extensions = ['py', ]  # '.pyc', '.pyo', '.pyw', '.pyx', '.pxd', '.pxi']

    paths = [path for path in gather_file_paths(sys.argv[1])
             if '.' in path and path.split('.')[-1] in valid_extensions]

    celery_process = multiprocessing.Process(target=start_worker, args=())
    celery_process.start()
    task_ids = start_scanning(paths)
    while task_ids:
        for task_id in task_ids:
            if task_id.ready():
                task_ids.remove(task_id)
                break
        else:
            print("Waiting for tasks to finish...")
            sleep(1)
    celery_process.terminate()

    return 0


def main() -> int:
    return deepsource()
