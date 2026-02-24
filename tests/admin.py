"""Admin configuration for test models."""

from djust_admin import DjustModelAdmin, register

from .models import Article, Author, Book, Category, Tag


@register(Category)
class CategoryAdmin(DjustModelAdmin):
    """Admin for Category model."""

    list_display = ["name"]
    search_fields = ["name"]


@register(Tag)
class TagAdmin(DjustModelAdmin):
    """Admin for Tag model."""

    list_display = ["name", "color"]
    search_fields = ["name"]


@register(Article)
class ArticleAdmin(DjustModelAdmin):
    """Admin for Article model with FK, M2M, and date fields."""

    list_display = ["title", "category", "status", "is_featured", "publish_date"]
    list_filter = ["status", "is_featured", "category"]
    search_fields = ["title", "content"]

    fieldsets = [
        (None, {"fields": ["title", "slug", "status"]}),
        ("Content", {"fields": ["content", "is_featured"]}),
        ("Classification", {"fields": ["category", "tags"]}),
        ("Publishing", {"fields": ["publish_date", "publish_time"]}),
    ]


@register(Author)
class AuthorAdmin(DjustModelAdmin):
    """Admin for Author model."""

    list_display = ["name", "email"]
    search_fields = ["name", "email"]


@register(Book)
class BookAdmin(DjustModelAdmin):
    """Admin for Book model with required FK."""

    list_display = ["title", "author", "publication_date", "pages"]
    list_filter = ["author"]
    search_fields = ["title"]

    fieldsets = [
        (None, {"fields": ["title", "author"]}),
        ("Details", {"fields": ["publication_date", "pages"]}),
    ]
