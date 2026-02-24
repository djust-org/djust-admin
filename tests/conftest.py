"""Pytest fixtures for djust-admin Playwright tests."""

import os
import subprocess
import sys
import time

import pytest
import requests

# Path to the test database file
TEST_DB_PATH = os.path.join(os.path.dirname(__file__), "test_db.sqlite3")


@pytest.fixture(scope="session")
def django_db_setup(django_db_blocker):
    """Set up the test database with migrations."""
    # Remove old database if exists
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    with django_db_blocker.unblock():
        from django.core.management import call_command

        call_command("migrate", "--run-syncdb", verbosity=0)

    yield

    # Cleanup after tests
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


@pytest.fixture(scope="session")
def session_admin_user(django_db_setup, django_db_blocker):
    """Create an admin user for testing at session scope.

    This user persists for the entire test session and is visible
    to the Django server subprocess.
    """
    with django_db_blocker.unblock():
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user, _ = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        user.set_password("adminpass123")
        user.save()
        return user


@pytest.fixture
def admin_user(session_admin_user):
    """Alias for session_admin_user to work with function-scoped tests."""
    return session_admin_user


class DjangoServer:
    """Manages a Django development server for Playwright tests."""

    def __init__(self, host="127.0.0.1", port=8765):
        self.host = host
        self.port = port
        self.process = None
        self.url = f"http://{host}:{port}"

    def start(self):
        """Start the Django development server with Daphne for WebSocket support."""
        # Start Daphne ASGI server (supports WebSocket for dj-click events)
        self.process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "daphne",
                "-b",
                self.host,
                "-p",
                str(self.port),
                "tests.asgi:application",
            ],
            env={**os.environ, "DJANGO_SETTINGS_MODULE": "tests.settings"},
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Wait for server to start and be ready
        for _ in range(30):
            try:
                response = requests.get(f"{self.url}/admin/login/", timeout=1)
                if response.status_code in (200, 302):
                    return
            except requests.exceptions.RequestException:
                pass
            time.sleep(0.5)

        # Check if server is running
        if self.process.poll() is not None:
            stdout, stderr = self.process.communicate()
            raise RuntimeError(
                f"Server failed to start:\nstdout: {stdout.decode()}\nstderr: {stderr.decode()}"
            )

    def stop(self):
        """Stop the Django development server."""
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()


@pytest.fixture(scope="session")
def django_server(session_admin_user):
    """Start a Django server for the test session.

    Depends on session_admin_user to ensure the user exists before starting.
    """
    server = DjangoServer()
    server.start()
    yield server
    server.stop()


# Override pytest-playwright's base_url fixture to use our Django server
@pytest.fixture(scope="session")
def base_url(django_server):
    """Get the base URL for the test server."""
    return django_server.url


@pytest.fixture(scope="session")
def admin_url(django_server):
    """Get the admin base URL."""
    return f"{django_server.url}/admin"


def create_test_data(django_db_blocker):
    """Helper to create test data in the shared database."""
    with django_db_blocker.unblock():
        from tests.models import Author, Category, Tag

        # Create categories
        cats = []
        for name in ["Technology", "Science", "Arts"]:
            cat, _ = Category.objects.get_or_create(name=name)
            cats.append(cat)

        # Create tags
        tag_data = [
            ("Python", "blue"),
            ("Django", "green"),
            ("JavaScript", "yellow"),
            ("Testing", "red"),
        ]
        tag_list = []
        for name, color in tag_data:
            tag, _ = Tag.objects.get_or_create(name=name, defaults={"color": color})
            tag_list.append(tag)

        # Create authors
        author_data = [
            ("Alice Smith", "alice@example.com"),
            ("Bob Jones", "bob@example.com"),
        ]
        authors = []
        for name, email in author_data:
            author, _ = Author.objects.get_or_create(name=name, defaults={"email": email})
            authors.append(author)

        return cats, tag_list, authors


@pytest.fixture(scope="session")
def session_test_data(django_db_setup, django_db_blocker):
    """Create shared test data at session scope."""
    return create_test_data(django_db_blocker)


@pytest.fixture
def categories(session_test_data):
    """Get test categories."""
    return session_test_data[0]


@pytest.fixture
def tags(session_test_data):
    """Get test tags."""
    return session_test_data[1]


@pytest.fixture
def authors(session_test_data):
    """Get test authors."""
    return session_test_data[2]


@pytest.fixture
def articles(categories, tags, django_db_blocker):
    """Create test articles."""
    with django_db_blocker.unblock():
        from tests.models import Article

        tech = categories[0]
        article, _ = Article.objects.get_or_create(
            slug="test-article",
            defaults={
                "title": "Test Article",
                "content": "This is test content",
                "status": "draft",
                "category": tech,
            },
        )
        article.tags.set([tags[0], tags[1]])
        return [article]


@pytest.fixture
def books(authors, django_db_blocker):
    """Create test books."""
    with django_db_blocker.unblock():
        from datetime import date

        from tests.models import Book

        book, _ = Book.objects.get_or_create(
            title="Test Book",
            defaults={
                "author": authors[0],
                "publication_date": date(2024, 1, 15),
                "pages": 250,
            },
        )
        return [book]




@pytest.fixture(scope="session")
def logged_in_context(browser, admin_url, session_admin_user, django_server):
    """Create a browser context with an authenticated session.

    This is session-scoped to share the login across ALL tests,
    avoiding repeated logins that can cause server issues.
    """
    # Create a new browser context
    context = browser.new_context()
    page = context.new_page()

    # Use the test login endpoint (traditional HTTP POST)
    base_url = django_server.url
    test_login_url = f"{base_url}/test-login/?next={admin_url}/"

    # Navigate to the test login form
    page.goto(test_login_url, wait_until="networkidle")

    # Fill the form and submit
    page.locator('input[name="username"]').fill("admin")
    page.locator('input[name="password"]').fill("adminpass123")

    # Click submit - don't wait for navigation since it might be intercepted
    page.locator('button[type="submit"]').click(no_wait_after=True)

    # Wait for redirect to admin URL
    page.wait_for_url(f"{admin_url}/**", timeout=30000)

    # Close the page but keep the context (with session cookies)
    page.close()

    yield context

    context.close()


@pytest.fixture
def logged_in_page(logged_in_context, admin_url):
    """Return a new page in the authenticated context."""
    page = logged_in_context.new_page()
    yield page
    page.close()
