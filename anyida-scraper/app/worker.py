from app.celery_app import celery_app
import sys

# This file can be used to run the worker via python app/worker.py
# But usually you run `celery -A app.celery_app worker --loglevel=info`

if __name__ == "__main__":
    # For Windows support (Celery 4+ on Windows needs this or pool=solo)
    # But since we are using 'celery' command usually, this script might just be a helper.
    # However, to support `python app/worker.py`:
    
    argv = [
        'worker',
        '--loglevel=INFO',
        '--pool=solo' # Important for Windows!
    ]
    celery_app.worker_main(argv)
