import db
import utilities
import random 

actors = db.Actor.objects()
print(actors)
for actor in actors:
    print(actor.name)
    scenes = db.Video.objects(actors=actor)
    video_reference = scenes.first()
    if video_reference:
        actor.update(set__image=random.choice(video_reference.screencaps),set__scenes=scenes.count())
