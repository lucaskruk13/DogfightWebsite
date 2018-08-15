from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from .models import Profile

@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ['handicap', 'bio']
    template_name = 'accounts/my_account.html'
    success_url = reverse_lazy('feed')

    def get_object(self, queryset=None):
        return self.request.user.profile

# @method_decorator(login_required, name='dispatch')
# class UserUpdateView(UpdateView):
#     model = User
#     fields = ('first_name', 'last_name', 'email',)
#     template_name = 'accounts/my_account.html'
#     success_url = reverse_lazy('my_account')
#
#     def get_object(self, queryset=None):
#         return self.request.user

# Create your views here.
def signup(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('my_account')
    else:
        form = SignUpForm()
    return render(request, 'Accounts/auth/signup.html', {'form': form})