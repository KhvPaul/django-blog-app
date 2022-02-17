from django.urls import path

from . import views

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog-list'),
    path('<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('create/', views.BlogCreateView.as_view(), name='blog-create'),
    path('<int:pk>/update/', views.BlogUpdateView.as_view(), name='blog-update'),
    path('<int:pk>/delete/', views.BlogDeleteView.as_view(), name='blog-delete'),
    path('blogger/<int:pk>/', views.BloggerDetailView.as_view(), name='blogger-detail'),
    path('blogger/<int:pk>/update/', views.BloggerUpdateFormView.as_view(), name='blogger-update'),
    path('<int:pk>/create/', views.CommentCreateFormView.as_view(), name='create-comment'),
    path('contact-us/', views.ContactUsFormView.as_view(), name='contact-us'),
    # path('contact-us/', views.contact_us_form, name='contact-us'),

]
