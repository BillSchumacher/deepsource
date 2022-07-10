from celery import Celery

app = Celery('DeepSource', quiet=True)

app.conf.update(
    accept_content=['json'],
    broker_transport_options={},
    broker_url='redis://localhost:6379/2',
    result_backend='redis://localhost:6379/2',
    result_backend_transport_options={},
    result_serializer='json',
    task_serializer='json',
    quiet=True,
)
