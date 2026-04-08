from django.db import models
from django.conf import settings
# settings.AUTH_USER_MODEL = our custom User model
# Always use this instead of importing User directly
# If we ever change the User model — this still works


class Category(models.Model):
    """
    Blog categories — e.g. Technology, Python, Django
    One category can have MANY posts
    """
    name = models.CharField(max_length=100, unique=True)
    # unique=True = no two categories with same name
    # e.g. can't have "Python" twice

    slug = models.SlugField(max_length=100, unique=True)
    # slug = URL-friendly version of name
    # "Django Tips" → "django-tips"
    # Used in URLs like /api/blog/posts/?category=django-tips

    description = models.TextField(blank=True)
    # blank=True = this field is optional
    # TextField = long text, no max length

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'categories'
        # verbose_name_plural = fixes admin panel showing "Categorys"
        # Now shows "Categories" correctly
        ordering = ['name']
        # Default ordering = alphabetical by name

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Blog post — the main content
    Each post belongs to ONE user (author) and ONE category
    """

    # Post status choices — like a dropdown
    # In real companies we always use choices for status fields
    class Status(models.TextChoices):
        DRAFT     = 'draft',     'Draft'
        PUBLISHED = 'published', 'Published'
        ARCHIVED  = 'archived',  'Archived'
    # Usage: post.status = Post.Status.PUBLISHED

    title = models.CharField(max_length=255)

    slug = models.SlugField(max_length=255, unique=True)
    # Unique slug for each post
    # "My First Django Post" → "my-first-django-post"

    content = models.TextField()
    # The actual blog content — long text

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
        # New posts start as DRAFT — not visible publicly
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
        # on_delete=CASCADE = if user is deleted, delete their posts too
        # related_name='posts' = lets us do user.posts.all()
        # to get all posts by a user — very useful!
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
        # SET_NULL = if category deleted, post stays but category becomes null
        # We don't want to lose posts if a category is deleted
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'posts'
        ordering = ['-created_at']
        # Newest posts first

    def __str__(self):
        return f"{self.title} by {self.author.full_name}"

    @property
    def comment_count(self):
        return self.comments.count()
        # self.comments = all comments on this post
        # .count() = total number
        # @property means we access it like post.comment_count (no parentheses)


class Comment(models.Model):
    """
    Comment on a blog post
    Each comment belongs to ONE post and ONE user
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
        # related_name='comments' = lets us do post.comments.all()
        # CASCADE = if post deleted, delete its comments too
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
        # CASCADE = if user deleted, delete their comments too
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comments'
        ordering = ['created_at']
        # Oldest comments first — like a real comment thread

    def __str__(self):
        return f"Comment by {self.author.full_name} on {self.post.title}"