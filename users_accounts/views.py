from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import FormView, View
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User

from users_accounts.forms import LoginForm, RegisterForm, ReactivationForm
from users_accounts.models import RegistrationToken
from users_accounts.utils import send_activation_email


class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        return HttpResponseRedirect(reverse_lazy('accounts:login'))

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        username = form.cleaned_data['username']

        user = User.objects.filter(username=username)
        if user.exists():
            user = user.first()
            if notuser.is_active:
                messages.error(self.request, 'Activate your account')
                return redirect('accounts:login')

        context['errors'] = form.errors
        return self.render_to_response(context)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        user_token = RegistrationToken.objects.create(user=user)

        send_activation_email(user, user_token, self.request)
        messages.success(self.request, 'You have to activate your account')
        return super(RegisterView, self).form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context['form_errors'] = form.errors
        return self.render_to_response(context)


class ActivateAccountView(View):
    def get(self, request, user_id, token):
        user = get_object_or_404(User, id=user_id)
        token = get_object_or_404(RegistrationToken, token=token, user=user)

        if not user.is_active and token.verify_token():
            user.is_active = True
            token.clear_token()
            user.save()

            messages.success(request, 'Activation complete')
            return redirect('accounts:login')

        messages.error(request, 'Token expired')
        return redirect('accounts:login')


class ReactivationSentView(FormView):
    template_name = 'accounts/reactivation_sent.html'
    form_class = ReactivationForm
    success_url = reverse_lazy('accounts:reactivation_sent')

    def form_valid(self, form):
        user = User.objects.get(email=form.cleaned_data['email'])

        if user.is_active:
            messages.warning(self.request, 'This account is already activate')
            return redirect('accounts:login')

        token = user.token
        token.delete()
        new_token = RegistrationToken.objects.create(user=user)
        send_activation_email(user, new_token, self.request)
        messages.success(self.request, 'new activation email has been sent. Please check your inbox')
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context['form-errors'] = form.errors
        return self.render_to_response(context)
