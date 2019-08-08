from threadedcomments.templatetags.threadedcomments_tags import RenderCommentListNode

from django import template

register = template.Library()


class RelatedRenderCommentListNode(RenderCommentListNode):
    def get_queryset(self, context):
        qs = super().get_queryset(context)
        return qs.select_related('user')


@register.tag
def render_comment_list(parser, token):
    return RelatedRenderCommentListNode.handle_token(parser, token)
