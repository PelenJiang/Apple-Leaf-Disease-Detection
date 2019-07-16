from django.db import models

# Create your models here.
class File(models.Model):
  
    file_name=models.CharField(max_length=100)
    file_size=models.IntegerField()
    create_time=models.DateTimeField(auto_now_add=True)
    file=models.ImageField(upload_to='static/upload')

    def __str__(self):
        return self.file_name
    class Meta:
        verbose_name='image'
        verbose_name_plural=verbose_name
