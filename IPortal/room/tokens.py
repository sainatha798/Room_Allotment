from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class Confirm_room_mail(PasswordResetTokenGenerator):
    def _make_hash_value(self, room,timestamp):
        return (six.text_type(room.pk) + six.text_type(timestamp) + six.text_type((room.is_filled)))