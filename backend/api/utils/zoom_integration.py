"""
Zoom SDK integration utilities.
"""

import requests
from django.conf import settings
import jwt
from datetime import datetime, timedelta


class ZoomAPI:
    """Zoom API integration class."""

    BASE_URL = "https://api.zoom.us/v2"

    def __init__(self):
        self.api_key = settings.ZOOM_API_KEY
        self.api_secret = settings.ZOOM_API_SECRET

    def generate_jwt_token(self):
        """Generate JWT token for Zoom API."""
        payload = {
            'iss': self.api_key,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload, self.api_secret, algorithm='HS256')
        return token

    def create_meeting(self, topic, start_time, duration, agenda=''):
        """
        Create a Zoom meeting.

        Args:
            topic: Meeting topic
            start_time: Start time (datetime object)
            duration: Duration in minutes
            agenda: Meeting agenda

        Returns:
            dict: Meeting details including join URL
        """
        url = f"{self.BASE_URL}/users/me/meetings"
        headers = {
            'Authorization': f'Bearer {self.generate_jwt_token()}',
            'Content-Type': 'application/json'
        }

        data = {
            'topic': topic,
            'type': 2,  # Scheduled meeting
            'start_time': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'duration': duration,
            'timezone': 'UTC',
            'agenda': agenda,
            'settings': {
                'host_video': True,
                'participant_video': True,
                'join_before_host': False,
                'mute_upon_entry': True,
                'watermark': False,
                'audio': 'both',
                'auto_recording': 'cloud',
                'waiting_room': True,
            }
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating Zoom meeting: {e}")
            return None

    def get_meeting(self, meeting_id):
        """Get meeting details."""
        url = f"{self.BASE_URL}/meetings/{meeting_id}"
        headers = {
            'Authorization': f'Bearer {self.generate_jwt_token()}'
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting Zoom meeting: {e}")
            return None

    def delete_meeting(self, meeting_id):
        """Delete a Zoom meeting."""
        url = f"{self.BASE_URL}/meetings/{meeting_id}"
        headers = {
            'Authorization': f'Bearer {self.generate_jwt_token()}'
        }

        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error deleting Zoom meeting: {e}")
            return False


def create_session_meeting(session):
    """
    Create Zoom meeting for a session.

    Args:
        session: Session model instance

    Returns:
        bool: Success status
    """
    zoom = ZoomAPI()

    topic = f"Quran Learning Session - {session.student.get_full_name()}"
    start_time = datetime.combine(session.scheduled_date, session.scheduled_time)
    duration = session.duration
    agenda = f"Curriculum: {session.curriculum}\nTopic: {session.lesson_topic}"

    meeting = zoom.create_meeting(topic, start_time, duration, agenda)

    if meeting:
        session.zoom_meeting_id = str(meeting['id'])
        session.zoom_meeting_password = meeting.get('password', '')
        session.zoom_join_url = meeting['join_url']
        session.zoom_start_url = meeting['start_url']
        session.save()
        return True

    return False
