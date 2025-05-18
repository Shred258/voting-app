from django.apps import AppConfig


class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'


class VotingAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'voting_app'
    
    def ready(self):
        from voting_app.startup import startup
        startup()