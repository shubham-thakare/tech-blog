from django.db import models


STATUS_CHOICES = (
    ("SN", "Seen"),
    ("UN", "Unseen"),
)


class Inbox(models.Model):
    name = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=50, null=False)
    message = models.TextField(max_length=1000, null=False)
    submitted_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=2,
                              default='UN')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Inbox"
