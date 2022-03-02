from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.utils.encoding import smart_text as smart_unicode
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class Todo(models.Model):
    """
        Needed fields
        - user (fk to User Model - Use AUTH_USER_MODEL from django.conf.settings)
        - name (max_length=1000)
        - done (boolean with default been false)
        - date_created (with default of creation time)
        - date_completed (set it when done is marked true)

        Add string representation for this model with todos name.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    done = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=datetime.now)
    date_completed = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.done and self.date_completed is None:
            self.pub_date = datetime.now()
        super(Todo, self).save(*args, **kwargs)
