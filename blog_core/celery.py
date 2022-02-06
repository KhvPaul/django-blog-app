# import os
#
# from celery import Celery
# from celery.schedules import crontab
#
# from django.conf import settings
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_core.settings')
#
# app = Celery('blog_core')
#
# app.config_from_object('django.conf:settings', namespace='CELERY')
#
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
#
# app.conf.beat_schedule = {
#     'notify-blogger-comment': {
#         'task': 'blog.tasks.task.comment_message',
#         'schedule': crontab(),
#     },
#     'notify-blogger-blog': {
#             'task': 'blog.tasks.task.blog_message',
#             'schedule': crontab(),
#         },
#     'news-parser': {
#         'task': 'blog.tasks.task.news_pasrer',
#         'schedule': crontab()
#         # 'schedule': crontab(hour='*/6'),
#     },
# }
