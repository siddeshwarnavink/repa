from celery import shared_task

@shared_task
def process_files_task(process_id):
    print("I got ran!")
    pass
