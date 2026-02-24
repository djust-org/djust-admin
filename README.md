# djust-admin

A modern, reactive Django admin interface powered by [djust](https://djust.org).

> **Status: Pre-Alpha** - This project is in early development. APIs may change.

## Features

- **Real-time search** - Filter results as you type with debounced queries
- **Live sorting** - Click columns to sort without page reload
- **Bulk actions** - Select multiple items and perform actions
- **Instant feedback** - Form validation and save feedback in real-time
- **Modern UI** - Clean, responsive design with Tailwind CSS
- **Django compatible** - Works with existing Django models and permissions

## Installation

```bash
pip install djust-admin
```

## Quick Start

### 1. Add to INSTALLED_APPS

```python
INSTALLED_APPS = [
    # ...
    'djust',
    'djust_admin',
    # ...
]
```

### 2. Create admin configuration

```python
# myapp/admin.py
from djust_admin import DjustModelAdmin, site

from .models import Article, Author

@site.register(Article)
class ArticleAdmin(DjustModelAdmin):
    list_display = ['title', 'author', 'published_date', 'status']
    list_filter = ['status', 'author']
    search_fields = ['title', 'content']
    ordering = ['-published_date']

@site.register(Author)
class AuthorAdmin(DjustModelAdmin):
    list_display = ['name', 'email', 'article_count']
    search_fields = ['name', 'email']

    def article_count(self, obj):
        return obj.articles.count()
    article_count.short_description = "Articles"
```

### 3. Add URLs

```python
# urls.py
from django.urls import path, include
from djust_admin import site

urlpatterns = [
    # ... your other urls
    path('djust-admin/', include(site.urls)),
]
```

### 4. Configure ASGI (for WebSocket support)

```python
# asgi.py
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from djust.websocket import LiveViewConsumer
from django.urls import path

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/live/', LiveViewConsumer.as_asgi()),
        ])
    ),
})
```

## Configuration

### DjustModelAdmin Options

```python
class MyModelAdmin(DjustModelAdmin):
    # List view
    list_display = ['field1', 'field2']      # Fields to show in list
    list_filter = ['status', 'created_at']   # Filter sidebar
    search_fields = ['title', 'content']     # Searchable fields
    list_per_page = 25                       # Items per page
    ordering = ['-created_at']               # Default ordering

    # Detail view
    fields = ['field1', 'field2']            # Fields to show in form
    readonly_fields = ['created_at']         # Non-editable fields
    fieldsets = [                            # Group fields
        ('Basic Info', {'fields': ['title', 'slug']}),
        ('Content', {'fields': ['body']}),
    ]

    # Actions
    actions = ['publish', 'archive']         # Bulk actions

    def publish(self, request, queryset):
        queryset.update(status='published')
    publish.short_description = "Publish selected"
```

### Custom Admin Site

```python
from djust_admin import DjustAdminSite

class MyAdminSite(DjustAdminSite):
    site_header = "My Company Admin"
    site_title = "Admin Portal"
    index_title = "Welcome to the Admin"

admin_site = MyAdminSite(name='myadmin')
```

## Comparison with Django Admin

| Feature | Django Admin | djust-admin |
|---------|--------------|-------------|
| Page reloads for actions | Yes | No (WebSocket) |
| Search | On submit | Real-time |
| Sorting | Page reload | Instant |
| Form validation | On submit | Real-time |
| Bulk selection | Checkbox + submit | Live state |
| JavaScript required | ~150KB | ~5KB |

## Roadmap

### v0.1.0 (Current)
- [x] Basic model list view with search/sort/pagination
- [x] Model detail/edit view with form validation
- [x] Delete confirmation
- [x] Bulk actions (delete)
- [ ] Filter sidebar

### v0.2.0
- [ ] Inline related objects
- [ ] Foreign key autocomplete
- [ ] File upload support
- [ ] Custom actions with confirmation

### v0.3.0
- [ ] Dashboard widgets
- [ ] Activity log
- [ ] User preferences
- [ ] Themes

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT License - see [LICENSE](LICENSE) for details.
