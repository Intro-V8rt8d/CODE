from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from django.db.models.signals import post_save
        from django.contrib.auth.models import User
        from .models import Profile

        def create_profile(sender, instance, created, **kwargs):
            if created:
                # Always create profile (no hasattr check needed because OneToOne ensures uniqueness)
                Profile.objects.create(user=instance, full_name=instance.get_username())

        post_save.connect(create_profile, sender=User)
