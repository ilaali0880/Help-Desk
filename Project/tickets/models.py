from django.db import models

# Create your models here.
class Ticket(models.Model):

    class Priority(models.TextChoices):
        LOW = 'L' , 'کم' 
        MEDIUM = 'M' , 'متوسط'
        HIGH = 'H' , 'زیاد'
    priority = models.CharField(
        max_length=1,
        choices= Priority.choices,
        default= Priority.LOW
    )

    class Status(models.TextChoices):
        OPEN = 'O' , 'باز'
        INPROGRESS = 'IP' , 'درحال بررسی'
        RESOLVED = 'R' , 'حل شده'
        CLOSED = 'C' , 'بسته شده'
    status = models.CharField(
        max_length=2,
        choices= Status.choices,
        default=Status.OPEN
    )

    class Category(models.TextChoices):
        HARDWARE = 'H' , 'سخت افزار'
        SOFTWARE = 'S' , 'نرم افزار'
        NETWORK = 'N' , 'شبکه'
        OTHER = 'OTH' , 'سایر'
    category = models.CharField(
        max_length=3,
        choices=Category.choices,
        default=Category.OTHER
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title   
  