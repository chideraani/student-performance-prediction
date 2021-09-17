from django.db import models

class FileUser(models.Model):
    userupload = models.FileField()
    title = models.CharField(max_length=50)

    def str(self):
        return self.title

class FileUser2(models.Model):
    userupload = models.FileField()
    titles = models.CharField(max_length=50)

    def str(self):
        return self.titles

