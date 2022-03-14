# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver




class Profile(models.Model):

    role_list = (
        (0, 'Пользователь'),
        (1, 'Администратор'),
        (2, 'Администратор системы'),
    )



    
    user = models.OneToOneField(User, verbose_name=u'Пользователь системы',on_delete=models.CASCADE,primary_key=True)
    name= models.CharField(blank=True,max_length=160, help_text="",verbose_name="ФИО",db_index=True)
    block = models.BooleanField(verbose_name=u'Заблокирован',null=False, default=False,blank=True)
    role = models.IntegerField(choices=role_list,blank=True,default=0,verbose_name="Роль пользователя") 
    api_client = models.BooleanField(verbose_name=u'api client',null=False, default=False,blank=True)
    isredonly=models.BooleanField(blank=True,default=False,verbose_name="Только просмотр")


    def get_client(self):
        return self.client

    def __unicode__(self):
        return self.user

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return str(self.user)

    class Meta:   # отображение в админики
        verbose_name = u'профиль'
        verbose_name_plural = u'профили'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        userClient=False
        Profile.objects.create(user=instance)
  

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()