from django.urls import path
from django.utils.translation import pgettext_lazy
from django.views.generic import TemplateView

app_name = 'manager'

urlpatterns = [
    path(pgettext_lazy("url", ''), TemplateView.as_view(template_name='manager/index2.html'), name='dashboard'),
    path(pgettext_lazy("url", 'user-profile'), TemplateView.as_view(template_name='manager/user-profile-lite.html'), name='user_profile'),
    path(pgettext_lazy("url", 'components-blogs'), TemplateView.as_view(template_name='manager/components-blog-posts.html'), name='components_blog_posts'),
    path(pgettext_lazy("url", 'components-blogs'), TemplateView.as_view(template_name='manager/components-blog-posts.html'), name='components_blog_posts'),
    path(pgettext_lazy("url", 'add-new-post'), TemplateView.as_view(template_name='manager/add-new-post.html'), name='add_new_post'),
    path(pgettext_lazy("url", 'form-components'), TemplateView.as_view(template_name='manager/form-components.html'), name='form_components'),
    path(pgettext_lazy("url", 'tables'), TemplateView.as_view(template_name='manager/tables.html'), name='tables'),
    path(pgettext_lazy("url", 'errors'), TemplateView.as_view(template_name='manager/errors.html'), name='errors'),
]
