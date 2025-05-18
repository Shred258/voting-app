from django.core.management import call_command
from django.db.utils import OperationalError
import os
import time

def startup():
    if 'RENDER' in os.environ:
        max_retries = 5
        retry_delay = 10
        
        for i in range(max_retries):
            try:
                call_command('migrate')
                from voting_app.settings import create_admin
                create_admin()
                break
            except (OperationalError, Exception) as e:
                print(f"Startup attempt {i+1} failed: {str(e)}")
                if i < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                raise

# Add to your app's __init__.py
default_app_config = 'voting_app.apps.VotingAppConfig'