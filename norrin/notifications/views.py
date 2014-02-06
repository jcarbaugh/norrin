import math

from django.shortcuts import render
from django.views.generic import View
from mongokit import Connection

from norrin.notifications import config
from norrin.notifications.models import Notification


conn = Connection(config.MONGODB_HOST, config.MONGODB_PORT)
db = conn[config.MONGODB_DATABASE]
if config.MONGODB_USERNAME and config.MONGODB_PASSWORD:
    db.authenticate(config.MONGODB_USERNAME, config.MONGODB_PASSWORD)


class StatusView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'recent_notifications': [n for n in db.notifications.find({}).limit(5).sort("timestamp", -1)],
        }
        return render(request, 'notifications/status.html', context)


class NotificationView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'notification': db.notifications.find_one({'id': kwargs.get('notification_id')})
        }
        return render(request, 'notifications/notification.html', context)


class NotificationListView(View):

    per_page = 20

    def get(self, request, *args, **kwargs):

        page = int(request.GET.get('page') or 1)
        offset = (page - 1) * self.per_page

        qs = db.notifications.find({})
        notifications = qs.sort('timestamp', -1).limit(self.per_page).skip(offset)

        total_count = qs.count()
        total_pages = int(math.ceil(total_count / float(self.per_page)))

        context = {
            'notifications': [n for n in qs],
            'pages': {
                'current': page,
                'total': total_pages,
                'next_page': page + 1 if page < total_pages else None,
                'previous_page': page - 1 if page > 1 else None,
            }
        }

        return render(request, 'notifications/notification_list.html', context)