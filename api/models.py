from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Campaign(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal_amount = models.IntegerField()
    raised_amount = models.IntegerField(default=0)
    image = models.URLField(default="https://picsum.photos/seed/default/800/400")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def progress(self):
        if self.goal_amount and self.goal_amount > 0:
            return round((self.raised_amount / self.goal_amount) * 100)
        return 0

    def _str_(self):
        return self.title

class Donation(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='donations')
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    donated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # update campaign total before saving donation
        if self.pk is None:  # new donation
            self.campaign.raised_amount = self.campaign.raised_amount + self.amount
            self.campaign.save()
        super().save(*args, **kwargs)

    def _str_(self):
        return f"{self.donor.username} -> {self.campaign.title} : {self.amount}"