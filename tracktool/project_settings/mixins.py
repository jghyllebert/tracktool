from django.core.mail import send_mail
from notifications.models import Notification, Receivers


class SendNotificationMixin(object):
    """
    Send notifications to select users
    """
    def send_notification(self, users, message):
        #Send notifications
        notification = Notification(
            message=message
        )
        notification.save()
        for user in users:
            receiver = Receivers(
                notification=notification,
                user=user,
            )
            receiver.save()

            #Send email if users agreed with it
            if user.email_notifications:
                send_mail(
                    'New notification from Tracktool',
                    notification.message,
                    self.request.user.email,
                    [user.email]
                )