nohup uvicorn server:app --host 0.0.0.0 --port 80 & nohup celery -A worker worker & tail -f nohup.out