from django.db import models
from apps.website.models.article import Article


STATUS_CHOICES = (
    ("SH", "Show"),
    ("HD", "Hide"),
)


class Comments(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=50, null=False)
    comments = models.TextField(max_length=2500, null=False)
    submitted_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=2,
                              default='SH')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Comments"
