from blog.forms import BloggerChangeForm, BloggerCreationForm, CommentCreateForm, ContactUsForm
from blog.models import Blog, Blogger, Comment

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
# from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic.list import MultipleObjectMixin

# from django.views.decorators.cache import cache_page

from .tasks.task import contact_us


class SignUpFormView(SuccessMessageMixin, generic.CreateView):
    model = get_user_model()
    form_class = BloggerCreationForm
    template_name = 'registration/signup.html'
    success_message = 'Successfully Updated User Profile'
    success_url = 'blog-list'

    def form_valid(self, form):
        form.save()
        user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))
        login(self.request, user)
        if self.request.GET and self.request.GET["next"] != "/accounts/login/":
            return HttpResponseRedirect(self.request.GET["next"])
        else:
            return redirect('blog-list')


class BloggerUpdateFormView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = get_user_model()
    form_class = BloggerChangeForm
    template_name = 'blog/blogger_form.html'
    success_message = 'Successfully Updated User Profile'

    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_object():
            logout(self.request)
            return redirect('login')

        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


class BloggerDetailView(generic.DetailView, MultipleObjectMixin):
    # queryset = Blogger.objects.prefetch_related(
    #     Prefetch(
    #         'blog_set',
    #         queryset=Blog.objects.all().order_by('-post_date')
    #     )
    # ).annotate(blogs_count=Count('blog'))
    model = Blogger
    paginate_by = 5

    def get_context_data(self, **kwargs):
        if self.request.user == self.get_object():
            object_list = Blog.objects.filter(blogger=self.get_object()).order_by('-post_date')
            context = super(BloggerDetailView, self).get_context_data(object_list=object_list, **kwargs)
        else:
            object_list = Blog.objects.filter(blogger=self.get_object(), is_posted=True).order_by('-post_date')
            context = super(BloggerDetailView, self).get_context_data(object_list=object_list, **kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        if Blogger.objects.get(pk=kwargs.get('pk')).is_staff:
            if not request.user.is_staff:
                # return reverse('blog-detail', kwargs={'pk': request.user.pk})
                return redirect('blog-list')
            else:
                if request.method.lower() in self.http_method_names:
                    handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
                else:
                    handler = self.http_method_not_allowed
                return handler(request, *args, **kwargs)
        else:
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            return handler(request, *args, **kwargs)


# @method_decorator(cache_page(30), name='dispatch')
class BlogListView(generic.ListView):
    queryset = Blog.objects.all().filter(is_posted=True).prefetch_related(
        'comment_set').annotate(comments_count=Count('comment'))
    paginate_by = 5
    ordering = ['-post_date']


# @method_decorator(cache_page(30), name='dispatch')
class BlogDetailView(generic.DetailView, MultipleObjectMixin):
    # queryset = Blog.objects.prefetch_related(
    #     Prefetch(
    #         'comment_set',
    #         queryset=Comment.objects.filter(is_posted=True)
    #     )
    # ).annotate(comments_count=Count('comment'))

    model = Blog
    paginate_by = 5

    def get_context_data(self, **kwargs):
        object_list = Comment.objects.filter(blog=self.get_object(), is_posted=True).order_by('-post_date')
        context = super(BlogDetailView, self).get_context_data(object_list=object_list, **kwargs)
        return context


class BlogCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Blog
    fields = ('title', 'content', 'publication_request')
    success_message = 'Blog successfully created'

    def get_success_url(self):
        return reverse('blog-detail', kwargs={'pk': Blog.objects.filter(blogger=self.request.user.pk).last()})

    def form_valid(self, form):
        blog = form.save(commit=False)
        blog.blogger = Blogger.objects.get(pk=self.request.user.pk)
        blog.save()
        # if blog.publication_request:
        #     message.delay(
        #         blog=blog.id,
        #         user=self.request.user.id,
        #     )
        return super(BlogCreateView, self).form_valid(form)


class BlogUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Blog
    fields = ('title', 'content', 'publication_request')
    success_message = 'Blog successfully updated'

    def dispatch(self, request, *args, **kwargs):
        if request.user != Blog.objects.get(pk=kwargs.get('pk')).blogger:
            logout(self.request)
            return redirect('login')

        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.is_posted = False
        form.instance.notified = False
        form.save()
        # if Blog.objects.get(pk=self.object.pk).publication_request:
        #     message.delay(
        #         blog=self.object.pk,
        #         blogger=self.request.user.id,
        #         updated=True
        #     )
        return super(BlogUpdateView, self).form_valid(form)


class BlogDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Blog
    success_message = 'Blog successfully deleted'
    success_url = reverse_lazy('blog-list')


class CommentCreateFormView(SuccessMessageMixin, generic.FormView):
    form_class = CommentCreateForm
    fields = ('blogger', "content")
    success_message = 'Comment successfully created'
    data = dict()

    # def get_success_url(self):
    #     return reverse('blog-detail', kwargs={'pk': self.object.blog.pk})

    # def form_valid(self, form):
    #     comment = form.save(commit=False)
    #     comment.blog = Blog.objects.get(pk=self.kwargs['pk'])
    #     comment.save()
    #     # message.delay(
    #     #     comment=comment.id,
    #     #     blogger=None,
    #     # )
    #     return super(CommentCreateView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        form = ContactUsForm()
        context = {'form': form, 'blog': Blog.objects.get(pk=self.kwargs['pk'])}

        self.data['html_form'] = render_to_string('blog/comment_form.html', context, request=request)
        return JsonResponse(self.data)

    # def post(self, request, *args, **kwargs):

    def form_valid(self, form):
        self.data['form_is_valid'] = True
        comment = form.save(commit=False)
        comment.blog = Blog.objects.get(pk=self.kwargs['pk'])
        comment.save()
        # message.delay(
        #     comment=comment.id,
        #     blogger=None,
        # )
        self.data['html_book_list'] = render_to_string('blog/blog_tmp.html', {
            'blog': Blog.objects.get(pk=self.kwargs['pk'])
        })
        return JsonResponse(self.data)


# class ContactUsFormView(SuccessMessageMixin, generic.FormView):
#     template_name = 'blog/contact_us.html'
#     form_class = ContactUsForm
#     success_url = reverse_lazy('blog-list')
#     success_message = 'Thank you for your feedback'
#
#     def get_initial(self):
#         if self.request.user.is_anonymous:
#             return {
#                 'email': ''
#             }
#         else:
#             return {
#                 'email': self.request.user.email
#             }
#
#     def form_valid(self, form):
#         # contact_us.delay(
#         #     email=form.cleaned_data.get('email'),
#         #     text=form.cleaned_data.get('text')
#         # )
#         return super(ContactUsFormView, self).form_valid(form)

# ???????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????


class ContactUsFormView(SuccessMessageMixin, generic.FormView):
    # template_name = 'blog/contact_us.html'
    form_class = ContactUsForm
    # success_url = reverse_lazy('blog-list')
    success_message = 'Thank you for your feedback'
    data = dict()

    def get_initial(self):
        if self.request.user.is_anonymous:
            return {
                'email': ''
            }
        else:
            return {
                'email': self.request.user.email
            }

    def get(self, request, *args, **kwargs):
        form = ContactUsForm(initial=self.get_initial())
        context = {'form': form}
        self.data['html_form'] = render_to_string('blog/contact_us.html', context, request=request)
        return JsonResponse(self.data)

    # def post(self, request, *args, **kwargs):

    def form_valid(self, form):
        self.data['form_is_valid'] = True
        contact_us.delay(
            email=form.cleaned_data.get('email'),
            text=form.cleaned_data.get('text')
        )
        return JsonResponse(self.data)


# def contact_us_form(request):
#     data = dict()
#     if request.method == 'POST':
#         form = ContactUsForm(request.POST)
#         if form.is_valid():
#             data['form_is_valid'] = True
#             data['html_book_list'] = render_to_string('blog/contact_us.html')
#             contact_us.delay(
#                                 email=form.cleaned_data.get('email'),
#                                 text=form.cleaned_data.get('text')
#                             )
#         else:
#             data['form_is_valid'] = False
#     else:
#         email = request.user.email if request.user.is_authenticated else ''
#         form = ContactUsForm(initial={'email': email})
#     context = {'form': form}
#     data['html_form'] = render_to_string('blog/contact_us.html', context, request=request)
#     return JsonResponse(data)


# ???????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????

class BloggerPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    success_message = 'Password successfully changed'
    template_name = 'registration/change-password.html'

    def get_success_url(self):
        return reverse('blogger-detail', kwargs={'pk': self.request.user.pk})
