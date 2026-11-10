from django.db import models

from django.db import models
from django.contrib.auth.models import User  # <-- Import the built-in User model

class Staff(models.Model):
    # This links the staff member directly to the logged-in manager account
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_staff', null=True, blank=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def initials(self):
        names = self.name.split()
        if len(names) >= 2:
            return f"{names[0][0]}{names[-1][0]}".upper()
        elif len(names) == 1:
            return names[0][:2].upper()
        return "ST"

# (Keep your Assignment model exactly the same below it!)


class Assignment(models.Model):
    STATUS_CHOICES = [
        ('IN_PROGRESS', 'In Progress'),
        ('ON_TIME', 'On Time'),
        ('LATE', 'Late Delivery'),
    ]

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    
    # New tracking metrics from your design
    time_given = models.TimeField(null=True, blank=True)
    time_delivered = models.TimeField(null=True, blank=True)
    expected_delivery = models.DateField(null=True, blank=True)
    date_delivered = models.DateField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IN_PROGRESS')
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.staff.name}"

