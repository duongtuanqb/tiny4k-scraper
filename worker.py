from celery.utils.log import get_task_logger
from celery import Celery
import lubed
import logging
import os
import db

celery_app = Celery('tasks', broker='amqp://localhost//')
logger = get_task_logger(__name__)

@celery_app.task
def crawlTask():
    lubed.Crawl()

@celery_app.task
def startScrape():
    try:
        tasks = db.Task.objects(processed=False)
        for task in tasks:
            scrapeTask.delay(task.url)
        return 'successful'
    except:
        logging.exception('err')
        return 'unsucessful'

@celery_app.task
def scrapeTask(url):
    try:
        new_video = lubed.Video(url)
        new_video.save()
        db.Task.objects(url=url).update_one(processed=True)
        return 'successful'
    except:
        logging.exception('err')
        return 'unsucessful'



