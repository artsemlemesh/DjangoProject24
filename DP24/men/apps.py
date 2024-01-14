from django.apps import AppConfig


class MenConfig(AppConfig):
    verbose_name = 'men of the world' # changes the header of the table in django admin panel
    default_auto_field = "django.db.models.BigAutoField"
    name = "men"
