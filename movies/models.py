from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.

class Movie(models.Model):
    MOVIE_TYPE = (
        ('fi', 'films'),
        ('se', 'series'),
        ('ca', 'cartoons'),
    )
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='image' ,null=True, blank=True)
    movie_type = models.CharField(default='films' ,max_length=200 ,choices=MOVIE_TYPE)
    category = models.ManyToManyField('Category', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=True)

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']

    def __str__(self):
        return self.title

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner_id', flat=True)
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up')
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes)
        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()
    


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=True)
    
    class Meta:
        unique_together = [['owner', 'movie']]
    
    def __str__(self):
        return self.value

class Category(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name
    