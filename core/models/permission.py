from django.db import models

from utils.ulid import generate_ulid


class Permission(models.Model):
    class Meta:
        db_table = 'permissions'

    permission_id = models.UUIDField(
        primary_key=True, editable=False, default=generate_ulid
    )

    code = models.CharField(max_length=20, unique=True, verbose_name='Code')
    description = models.TextField(verbose_name='Description')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')

    def __str__(self):
        return self.code
