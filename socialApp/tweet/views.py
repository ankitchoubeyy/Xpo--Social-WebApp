from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.

def index(request):
    return render(request, 'index.html')


# Post list
def tweet_list(request):
    tweets = Post.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets})

# Post form
@login_required
def tweet_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = PostForm()
    return render(request, 'tweet_form.html', {'form': form})

# Post Edit
@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Post, pk=tweet_id, user = request.user)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
        pass
    else:
        form = PostForm(instance=tweet)
    return render(request, 'tweet_form.html', {"form": form})


# Delete Post
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Post, pk=tweet_id, user= request.user)
    if request.method == "POST":
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})


# # User registration form
# def register(request):
#     if request.mehthod == "POST":
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password'])
#             user.save()
#             login(request, user)
#     else:
#         form = UserRegistrationForm()
        
#     return render(request, 'registration/register.html')