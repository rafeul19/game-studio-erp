from django.db import models
from accounts.models import User
from erp_projects.models import Project

class Asset(models.Model):
    ASSET_TYPES = [
        ('3D', '3D Model'),
        ('2D', '2D Art'),
        ('AUDIO', 'Audio/SFX'),
        ('VFX', 'Visual Effects'),
        ('OTHER', 'Other'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES, default='OTHER')
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='assets'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_assets'
    )
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.asset_type}] {self.name}"

    def get_latest_version(self):
        return self.versions.order_by('-version_number').first()


class AssetVersion(models.Model):
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name='versions'
    )
    version_number = models.PositiveIntegerField()
    file = models.FileField(upload_to='assets/%Y/%m/%d/', null=True, blank=True)
    file_path = models.CharField(max_length=500, blank=True, help_text="S3 Key or external URL")
    file_size = models.BigIntegerField(null=True, blank=True)
    file_type = models.CharField(max_length=50, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/%Y/%m/%d/', null=True, blank=True)
    note = models.TextField(blank=True, help_text="Release notes for this version")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='asset_uploads'
    )

    class Meta:
        ordering = ['-version_number']
        unique_together = ('asset', 'version_number')

    def __str__(self):
        return f"{self.asset.name} - v{self.version_number}"
