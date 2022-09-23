from django import template

from comments.models import Comment

register = template.Library()


@register.simple_tag
def get_children_comments(comment):
    comment_list = Comment.objects.filter(parent_comment=comment)
    return comment_list


@register.inclusion_tag('comments/comment.html')
def load_comment(comment):
    return {'comment': comment}


@register.simple_tag
def multiply(num1, num2):
    return num1 * num2


@register.simple_tag
def get_len_of_list(target_list):
    return len(target_list)