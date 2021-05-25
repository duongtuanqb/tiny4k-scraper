import db
import utilities

videos = db.Video.objects(slug__exists=False)
print(videos)
for video in videos:
    print(video)
    video.update(set__slug=utilities.generateSlug(video.title))
