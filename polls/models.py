from django.db import models
from django.utils import timezone
import datetime
# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class SurveyResult(models.Model):
    pop_preference = models.CharField(max_length=50)
    movement_preference = models.CharField(max_length=50)
    company_preference = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


    

class Review(models.Model):
    store = models.CharField(max_length=100)
    review = models.TextField()

    def __str__(self):
        return self.review