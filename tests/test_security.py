import pytest
from app import db
from app.models import Ticket
from werkzeug.security import generate_password_hash


def login(client, identifier, password):
    return client.post(
        '/login',
        data={'identifier': identifier, 'password': password},
        follow_redirects=True
    )


@pytest.fixture
def ticket(app, admin_user):
    # Create a ticket by admin for testing
    t = Ticket(
        title="Safe Ticket",
        description="Safe description",
        status="Open",
        created_by=admin_user.id,
        assigned_to=admin_user.id
    )
    db.session.add(t)
    db.session.commit()
    return t


def test_sql_injection_ticket_creation(client, admin_user):
    """
    Attempt SQL injection in the ticket title.
    The app should treat it as literal text, escaping special characters.
    """
    login(client, admin_user.username, 'adminpass')
    payload = "'; DROP TABLE ticket;--"
    response = client.post(
        '/tickets/create',
        data={
            'title': payload,
            'description': 'Injection test',
            'status': 'Open',
            'assigned_to': str(admin_user.id)
        },
        follow_redirects=True
    )
    assert response.status_code == 200

    # Jinja2 escapes apostrophes to &#39;, so check for the escaped payload
    escaped = "&#39;; DROP TABLE ticket;--".encode()
    assert escaped in response.data

    # Verify the tickets table still exists
    assert Ticket.query.count() >= 1


def test_xss_protection_in_comments(client, admin_user, ticket):
    """
    Submit an XSS payload as a comment.
    The <script> tags must be HTML-escaped.
    """
    login(client, admin_user.username, 'adminpass')

    xss_payload = "<script>alert('XSS')</script>"
    response = client.post(
        f'/tickets/{ticket.id}/comment',
        data={'comment': xss_payload},
        follow_redirects=True
    )
    assert response.status_code == 200

    # The script tags themselves should be escaped
    assert b"&lt;script&gt" in response.data
    assert b"&lt;/script&gt" in response.data

    # The raw payload must never appear unescaped
    assert xss_payload.encode() not in response.data
