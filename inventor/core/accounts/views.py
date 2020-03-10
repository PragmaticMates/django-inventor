from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import UpdateView, ListView, CreateView, DetailView, DeleteView
from pragmatic.mixins import LoginPermissionRequiredMixin, DeleteObjectMixin
# from inventor.core.accounts.filters import UserFilter
from inventor.core.accounts.forms import UpdateProfileForm, UserForm
from inventor.core.accounts.models import User


class UserDetailView(LoginPermissionRequiredMixin, DetailView):
    model = User
    permission_required = 'accounts.view_user'


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UpdateProfileForm
    template_name = 'accounts/user_profile_form.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, _('Profile successfully saved'))
        return super(UpdateProfileView, self).form_valid(form)

    def get_success_url(self):
        return self.request.user.get_absolute_url()


class UserUpdateView(LoginPermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    permission_required = 'accounts.change_user'

    def form_valid(self, form):
        messages.success(self.request, _('User successfully saved'))
        return super(UserUpdateView, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


# class UserListView(LoginPermissionRequiredMixin, ListView):
#     model = User
#     paginate_by = 10
#     permission_required = 'accounts.list_user'
#
#     def get_queryset(self):
#         return self.filter.qs.select_related('team').prefetch_related('groups')
#
#     def dispatch(self, request, *args, **kwargs):
#         self.filter = UserFilter(request.GET, queryset=self.get_whole_queryset())
#         return super(UserListView, self).dispatch(request, *args, **kwargs)
#
#     def get_whole_queryset(self):
#         return User.objects.all()
#
#     def get_context_data(self, **kwargs):
#         context_data = super(UserListView, self).get_context_data(**kwargs)
#         context_data['filter'] = self.filter
#         return context_data


class UserCreateView(LoginPermissionRequiredMixin, CreateView):
    model = User
    template_name = 'accounts/user_create.html'
    form_class = UserForm
    permission_required = 'accounts.add_user'

    def form_valid(self, form):
        user = form.save()

        # generate random user password
        password = User.objects.make_random_password()
        user.set_password(password)

        # send password to user
        user.email_user(_('Welcome to TatryTravel.sk'), _('Your password is {}').format(password), fail_silently=False)

        messages.success(self.request, _('User successfully created'))
        return super(UserCreateView, self).form_valid(form)


class UserDeleteView(LoginPermissionRequiredMixin, DeleteObjectMixin, DeleteView):
    model = User
    success_url = reverse_lazy('accounts:user_list')
    template_name = 'confirm_delete.html'
    permission_required = 'accounts.delete_user'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object() == self.request.user:
            messages.error(request, _("You can't delete your own account"))
            return redirect(reverse('accounts:user_list'))
        return super(UserDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, _('User successfully deleted'))
        return super(UserDeleteView, self).delete(request, *args, **kwargs)
