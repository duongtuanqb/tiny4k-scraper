from fastapi import FastAPI
import worker
import db

app = FastAPI(
    docs_url=None,
    redoc_url=None
)


@app.get('/api/crawl')
def crawl():
    try:
        worker.crawlTask.delay()
        return {
            'status' : 'ok',
            'message' : 'job added successfully'
        }
    except Exception as exception:
        return {
            'status' : 'failed',
            'message' : f'err - {exception}'
        }

@app.get('/api/start-tasks')
def startTasks():
    try:
        worker.startScrape.delay()
        return {
            'status' : 'ok',
            'message' : 'job added successfully'
        }
    except Exception as exception:
        return {
            'status' : 'failed',
            'message' : f'err - {exception}'
        }

@app.get('/api/progress')
def progress():
    done = db.Task.objects(processed = True).count()
    processing = db.Task.objects(processed = False).count()
    return {
        'total' : done+processing,
        'processing' : processing,
        'done' : done
    }
