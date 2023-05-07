from django.db import models

class Review(models.Model):
    store = models.CharField(max_length=100)
    review = models.TextField()
    prediction = models.TextField()


    def __str__(self):
        return self.review