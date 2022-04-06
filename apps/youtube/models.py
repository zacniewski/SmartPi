from django.db import models


class Song(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=100)
    downloaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"
