apt-get update
apt-get install python3 python3-pip rabbitmq-server
pip3 install uvicorn fastapi celery pydrive pymongo mongoengine tqdm dnspython bs4 
pip3 install httplib2==0.15.0
pip3 install google-api-python-client==1.6
touch nohup.out