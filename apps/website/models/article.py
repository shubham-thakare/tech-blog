from django.db import models


STATUS_CHOICES = (
    ("d", "Draft"),
    ("p", "Published"),
    ("w", "Withdrawn")
)


class Article(models.Model):
    page_name = models.CharField(max_length=500, null=False)
    title = models.CharField(max_length=500, null=False)
    keywords = models.CharField(max_length=1000, null=False)
    description = models.CharField(max_length=1000, null=False)
    public_image = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    read_time = models.CharField(max_length=20, null=False,
                                 default='1 min read')
    views = models.IntegerField(default=0, null=False)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1)
