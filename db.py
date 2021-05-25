from mongoengine import Document, connect
from mongoengine.fields import BooleanField, ReferenceField, StringField, ListField

connect('nhulan',host='mongodb+srv://admin:Acbdf123456789@nhulan.9uzw5.mongodb.net/tiny4k?retryWrites=true&w=majority')
# connect('nhulan')

class Studio(Document):
    name = StringField(required=True, unique=True)


class Actor(Document):
    name = StringField(required=True, unique=True)


class Category(Document):
    name = StringField(required=True, unique=True)


class Image(Document):
    url = StringField(required=True, unique=True)
    preview_url = StringField(required=True)


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

class Task(Document):
    url = StringField(required=True,unique=True)
    processed = BooleanField(required=True)