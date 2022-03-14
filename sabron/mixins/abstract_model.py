import uuid
from django.db import models


class AbstractUUID(models.Model):
    """ Абстрактная модель для использования UUID в качестве PK."""

    # Параметр blank=True позволяет работать с формами, он никогда не
    # будет пустым, см. метод save()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
