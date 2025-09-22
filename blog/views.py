from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Post, Comment
from .forms import CommentForm


# Create your views here.


class PostList(generic.ListView):
    """
    Uses Django generic view list to display posts on index page paginated by 6.
    """

    queryset = Post.objects.filter(status=1)
    template_name = "blog/index.html"
    paginate_by = 6


def post_detail(request, slug):
    """
    Display an individual :model:`blog.Post` with comments and comment submission form.

    Retrieves a published post by slug and displays it along with all associated
    comments. Handles comment submission via POST request, saving new comments
    with approval required status.

    **Context Variables:**
        ``post``
            An instance of :model:`blog.Post` - the blog post to display.
        ``comments``
            QuerySet of :model:`blog.Comment` - all comments for this post,
            ordered by creation date (newest first).
        ``comment_count``
            Integer count of approved comments for this post.
        ``comment_form``
            Instance of :form:`blog.CommentForm` - form for submitting new comments.

    **Template:**
        :template:`blog/post_detail.html`
    """

    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.add_message(
                request, messages.SUCCESS, "Comment submitted and awaiting approval"
            )
    comment_form = CommentForm()

    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
        },
    )


def comment_edit(request, slug, comment_id):
    """
    Handle editing of an existing comment.

    Allows authenticated users to edit their own :model:`blog.Comment`. The edited comment
    is automatically set to unapproved status and requires re-approval by
    an administrator. Only processes POST requests.

    **Returns:**
        HttpResponseRedirect: Redirects to the post detail page after processing.
    """
    if request.method == "POST":

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, "Comment Updated!")
        else:
            messages.add_message(request, messages.ERROR, "Error updating comment!")

    return HttpResponseRedirect(reverse("post_detail", args=[slug]))


def comment_delete(request, slug, comment_id):
    """
    Handle deletion of an existing comment.

    Allows authenticated users to delete their own :model:`blog.Comment`. The comment
    is permanently removed from the database. Users can only delete comments
    they authored.

    **Returns:**
        HttpResponseRedirect: Redirects to the post detail page after processing.
    """
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, "Comment deleted!")
    else:
        messages.add_message(request, messages.ERROR, "You can only delete your own comments!")

    return HttpResponseRedirect(reverse("post_detail", args=[slug]))
