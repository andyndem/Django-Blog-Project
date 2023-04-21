from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post


class PostListView(ListView):
  model = Post
  template_name = 'blog/home.html'  # Template to look for <app>/<model>_<viewtype>.html 
  context_object_name = 'posts'
  ordering = ['-date_posted']
  paginate_by = 5
  
class UserPostListView(ListView):
  model = Post
  template_name = 'blog/user_posts.html'  # Template to look for <app>/<model>_<viewtype>.html 
  context_object_name = 'posts'
  paginate_by = 5
  
  def get_queryset(self):
    user = get_object_or_404(User, username=self.kwargs.get('username'))
    return Post.objects.filter(author=user).order_by('-date_posted')
  
  
class PostDetailView(DetailView):
  model = Post
  
class PostCreateView(LoginRequiredMixin, CreateView):
  model = Post
  fields = ['title', 'content']
  # set success url attribute to redirect to home page here if needed
  
  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Post
  fields = ['title', 'content']
  # set success url attribute to redirect to home page here if needed
  
  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)
  
  def test_func(self): # prevent just any user from updating others' post
    post = self.get_object()
    if self.request.user == post.author:
      return True
    return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Post
  success_url = '/'
  
  def test_func(self): # prevent just any user from deleting others' posts
    post = self.get_object()
    if self.request.user == post.author:
      return True
    return False
  

# def home(request):
#   context = {
#   'posts': Post.objects.all()
# }
#   return render(request, 'blog/home.html', context)

def about(request):
  return render(request, 'blog/about.html', {'title': 'About'})
  
#  Initial implementations below
  
  # def home(request):
#   return render(request, 'blog/home.html')


# def about(request):
#   return render(request, 'blog/about.html')


# posts = [
#   {
#     'author': 'AniediAbasi',
#     'title': 'Blog Post 1',
#     'content': 'First post content.......',
#     'date_posted': 'March 15, 2023'
#   },
  
#   {
#     'author': 'CoreyM',
#     'title': 'Blog post 2',
#     'content': 'Inspired by Shaffer.......',
#     'date_posted': 'March 15, 2017'
#   },
  
#   {
#     'author': 'Trinity',
#     'title': 'Blog Post 3',
#     'content': 'All about Planets .......',
#     'date_posted': 'March 3, 2023'
#   },
# ]
