from django.db import models
from django.urls import reverse
from apps.website.models.authors import Authors


STATUS_CHOICES = (
    ("d", "Draft"),
    ("p", "Published"),
    ("w", "Withdrawn")
)


class Article(models.Model):
    author = models.ForeignKey(Authors, on_delete=models.DO_NOTHING,
                               null=True, blank=False)
    page_name = models.CharField(max_length=500, null=True, blank=True)
    title = models.CharField(max_length=500, null=False)
    keywords = models.CharField(max_length=1000, null=False)
    description = models.CharField(max_length=1000, null=False)
    public_image = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    read_time = models.CharField(max_length=20, null=True)
    views = models.IntegerField(default=0, null=False)
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=1, null=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article_base", args=[self.id, self.page_name])
