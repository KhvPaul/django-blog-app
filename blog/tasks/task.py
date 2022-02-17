from datetime import datetime


# from blog.models import Blog, Blogger, Comment

# from bs4 import BeautifulSoup

from celery import shared_task

from django.core.mail import send_mail

# import requests


@shared_task
def message(blogger, blog: str = None, comment: str = None, updated: bool = False):
    text = f'Blog id({blog})' if blog else f'Comment id({comment})'
    result = 'updated' if updated else 'added'
    user = f' by user({blogger})' if blogger else ''
    send_mail(
        'FIY',
        f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: {text} was {result}{user}',
        "khv.django.mail@gmail.com",
        ['khv.django.mail2@gmail.com'],
        fail_silently=False,
    )


# @shared_task
# def blog_message():
#     blogs = Blog.objects.filter(notified=False)
#     for blog in blogs:
#         if blog.is_posted:
#             send_mail(
#                 'FIY',
#                 f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}:'
#                 f' Blog({blog.pk}) was successfully posted after review.',
#                 "khv.django.mail2@gmail.com",
#                 [blog.blogger.email],
#                 fail_silently=False,
#             )
#             blog.notified = True
#             blog.save()
#
#
# @shared_task
# def comment_message():
#     comments = Comment.objects.filter(notified=False)
#     for comment in comments:
#         if comment.is_posted:
#             send_mail(
#                 'FIY',
#                 f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}:'
#                 f' A comment has been added to your blog{comment.blog.title} \n '
#                 f'Comment: {comment.content}. \n',
#                 f'link: http://127.0.0.1:8000/{comment.blog.get_absolute_url()}'
#                 "khv.django.mail2@gmail.com",
#                 [comment.blog.blogger.email],
#                 fail_silently=False,
#             )
#             comment.notified = True
#             comment.save()
#
#
# @shared_task()
# def news_pasrer():
#     # https: // www.president.gov.ua / ru
#     r = requests.get('https://www.president.gov.ua/ru')
#     if r.status_code == 200:
#         soup = BeautifulSoup(r.text, features="html.parser").find_all('div', {'class': 'item_text'})
#         soup2 = BeautifulSoup(r.text, features="html.parser").find_all('div', {'class': 'item_short middle_text'})
#         for i in range(len(soup2)):
#             blog = Blog.objects.filter(title=soup[i].find('a').text)
#             if not blog:
#                 Blog.objects.create(
#                     blogger=Blogger.objects.get(pk=3),
#                     title=soup[i].find('a').text,
#                     content=soup2[i].find('p').text,
#                     is_posted=True,
#                     publication_request=True,
#                     notified=True,
#                 )
#                 send_mail(
#                     'FIY',
#                     f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}:'
#                     'A new article from the site gov.ua has been successfully added.',
#                     "khv.django.mail2@gmail.com",
#                     ["khv.django.mail2@gmail.com"],
#                     fail_silently=False,
#                 )
#
#
@shared_task()
def contact_us(email, text):
    send_mail(
        f'FIY from {email}',
        f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: '
        f'{text}',
        "khv.django.mail2@gmail.com",
        ["khv.django.mai2l@gmail.com"],
        fail_silently=False,
    )
