from django.db import models
from django_extensions.db.fields import UUIDField

FLAGS = (
    ('requested', 'requested'),
    ('retrieved', 'retrieved'),
    ('transit', 'transit'),
    ('completed', 'completed'),
    ('error', 'error')
)

class FixedUUIDField(UUIDField):
    def pre_save(self, model_instance, add):
        value = super(UUIDField, self).pre_save(model_instance, add)
        if self.auto and add and not value:
            value = unicode(self.create_uuid())
            setattr(model_instance, self.attname, value)
        return value

class Request(models.Model):
    id = FixedUUIDField(primary_key=True)
    request_type = models.CharField(max_length=255)
    storage_type = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    target = models.CharField(max_length=255)
    request_date = models.DateField(auto_now_add=True)
    flag = models.CharField(max_length=20, default='requested', choices=FLAGS)
    action_date = models.DateField(null=True)

    def __unicode__(self):
        return self.id + ' ' + self.request_type + ' ' + self.action