from django.db import models
from django.contrib.auth.models import User
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

    requester = models.ForeignKey(User,on_delete=models.CASCADE,related_name='created_tickets')
    assigned_to = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='assigned_tickets')


    def __str__(self):
        return self.title   
class Comment(models.Model):
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE,related_name='comment')
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='author')
    message= models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.author}'