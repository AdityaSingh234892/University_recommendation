from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    Your_country = models.CharField(max_length=50, default='India')
    country = models.CharField(max_length=50)
    board = models.CharField(max_length=50)
    degree = models.CharField(max_length=50)
    bachelors_course = models.CharField(max_length=100, null=True, blank=True)
    bachelors_percentage = models.CharField(max_length=10, null=True, blank=True)
    toefl_score = models.CharField(max_length=100, null=True, blank=True)
    gre_score = models.CharField(max_length=100, null=True, blank=True)
    gpa_score = models.CharField(max_length=100, null=True, blank=True)
    twelveth_percentage = models.CharField(max_length=5)
    tenth_percentage = models.CharField(max_length=5)
    preferred_course = models.CharField(max_length=100)

    def __str__(self):
        return self.name
