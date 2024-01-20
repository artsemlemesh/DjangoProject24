from django.contrib.auth.models import AbstractUser
from django.db import models

#what if we need to keep extra data of a user, such as photo and so on, that is how we can solve it:
#extension of User model:
#1)create one more model (Profile, one-to-one field) with User Model
#2)create new model User based on the special class AbstractUser (code below)
#comment from youtube: Спасибо. Наконец-то узнал почему стоит использовать get_user_model а не просто обращаться к User. В некоторых обучающих видео видел что используют get_user_model, но почему её использовали, никто не объяснял


class User(AbstractUser):
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, null=True, verbose_name='photo')
    data_birth = models.DateTimeField(blank=True, null=True, verbose_name='date of birth')
#after applying migrations our standard model User will have two extra fields: photo, data_birth
#!!!IMPORTANT: WHEREVER WE WROTE USER, WE NEED TO REPLACE BY get_user_model() - it returns the current model, by the parameter redefined in settings: AUTH_USER_MODEL = "users.User", it checks which model is being used, and returns the proper model