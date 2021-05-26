from mongoengine import Document, connect
from mongoengine.fields import BooleanField, FloatField, IntField, ReferenceField, StringField, ListField

connect('nhulan',host='mongodb+srv://admin:Acbdf123456789@nhulan.9uzw5.mongodb.net/tiny4k?retryWrites=true&w=majority')
# connect('nhulan')

class Studio(Document):
    name = StringField(required=True, unique=True)
    meta = {'indexes': [
        {'fields': ['$name'],
         'default_language': 'english',
        }
    ]}

class Category(Document):
    name = StringField(required=True, unique=True)
    meta = {'indexes': [
        {'fields': ['$name'],
         'default_language': 'english',
        }
    ]}

class Image(Document):
    url = StringField(required=True, unique=True)
    preview_url = StringField(required=True)

class Actor(Document):
    name = StringField(required=True, unique=True)
    image = ReferenceField(Image)
    scenes = IntField(min_value=0)
    meta = {'indexes': [
        {'fields': ['$name'],
         'default_language': 'english',
        }
    ]}

class Video(Document):
    title = StringField(required=True)
    url = StringField(required=True, unique=True)
    slug = StringField(required=True)
    thumbnail = ReferenceField(Image)
    drive = StringField(required=True)
    studio = ReferenceField(Studio)
    actors = ListField(ReferenceField(Actor))
    category = ListField(ReferenceField(Category))
    screencaps = ListField(ReferenceField(Image))
    pictures = ListField(ReferenceField(Image))
    views = IntField(min_value=0)
    rating = FloatField(min_value=0)
    meta = {'indexes': [
        {'fields': ['$title', "$actors",'$slug'],
         'default_language': 'english',
        }
    ]}

class Task(Document):
    url = StringField(required=True,unique=True)
    processed = BooleanField(required=True)