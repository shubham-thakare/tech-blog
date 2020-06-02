from django.db import models
from django.urls import reverse


STATUS_CHOICES = (
    ("AC", "Active"),
    ("IN", "Inactive"),
)


class Authors(models.Model):
    dp = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=50, null=False)
    linkedIn_profile = models.CharField(max_length=50, null=True, blank=True)
    facebook_profile = models.CharField(max_length=50, null=True, blank=True)
    twitter_profile = models.CharField(max_length=50, null=True, blank=True)
    github_profile = models.CharField(max_length=50, null=True, blank=True)
    profession = models.CharField(max_length=100, null=False)
    bio = models.TextField(max_length=3000, null=False)
    joined_at = models.DateTimeField(null=False)
    status = models.CharField(choices=STATUS_CHOICES, max_length=2,
                              default='AC')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("author_profile", args=[self.id, self.name])

    class Meta:
        verbose_name_plural = "Authors"
