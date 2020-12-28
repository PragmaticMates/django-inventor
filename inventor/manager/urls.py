from django.urls import path
from django.utils.translation import pgettext_lazy
from django.views.generic import TemplateView

app_name = 'manager'

urlpatterns = [
    path(pgettext_lazy("url", ''), TemplateView.as_view(template_name='manager/index2.html'), name='manager_dashboard'),
    path('admin-user-profile', TemplateView.as_view(template_name='admin/user-profile-lite.html'), name='admin_user_profile'),
    path('admin-components-blogs', TemplateView.as_view(template_name='admin/components-blog-posts.html'), name='admin_components_blog_posts'),
    path('admin-components-blogs', TemplateView.as_view(template_name='admin/components-blog-posts.html'), name='admin_components_blog_posts'),
    path('admin-add-new-post', TemplateView.as_view(template_name='admin/add-new-post.html'), name='admin_add_new_post'),
    path('admin-form-components', TemplateView.as_view(template_name='admin/form-components.html'), name='admin_form_components'),
    path('admin-tables', TemplateView.as_view(template_name='admin/tables.html'), name='admin_tables'),
    path('admin-errors', TemplateView.as_view(template_name='admin/errors.html'), name='admin_errors'),
]
