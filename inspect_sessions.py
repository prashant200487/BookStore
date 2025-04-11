import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore.settings')
django.setup()

from django.contrib.sessions.models import Session

sessions = Session.objects.all()

for session in sessions:
    try:
        session_data = session.get_decoded()
        print(f"Session Key: {session.session_key}")
        print(f"Session Data: {session_data}")
    except Exception as e:
        print(f"Error decoding session {session.session_key}: {e}")