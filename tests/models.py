"""Test models for djust-admin Playwright tests."""

from django.db import models


class Category(models.Model):
    """Simple model for FK testing."""

    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Simple model for M2M testing."""

    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default="blue")

    def __str__(self):
        return self.name


class Article(models.Model):
    """Model with FK, M2M, and date fields for comprehensive testing."""

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
        ("archived", "Archived"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    is_featured = models.BooleanField(default=False)

    # ForeignKey field
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
    )

    # ManyToMany field
    tags = models.ManyToManyField(Tag, blank=True, related_name="articles")

    # Date fields
    publish_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Time field
    publish_time = models.TimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Author(models.Model):
    """Model for testing required FK fields."""

    name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    """Model with required FK for testing validation."""

    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    publication_date = models.DateField()
    pages = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
