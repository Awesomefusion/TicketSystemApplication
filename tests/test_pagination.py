import pytest
from app import db
from app.models import Ticket
from datetime import datetime

# reuse your login helper (or copy it here)
def login(client, identifier, password):
    return client.post(
        '/login',
        data={'identifier': identifier, 'password': password},
        follow_redirects=True
    )

@pytest.fixture
def many_tickets(app, admin_user):
    """
    Create 25 tickets so that we can test pagination:
    default per_page = 10 gives 3 pages (10,10,5).
    """
    for i in range(25):
        t = Ticket(
            title=f"Ticket {i+1}",
            description="Pagination test",
            status="Open",
            created_by=admin_user.id,
            assigned_to=admin_user.id
        )
        db.session.add(t)
    db.session.commit()
    # no return needed

def count_list_items(html):
    """Rough count of <li> in the tickets list"""
    return html.count('<li>')

def test_default_page_shows_10(client, admin_user, many_tickets):
    login(client, admin_user.username, 'adminpass')
    resp = client.get('/tickets/')
    assert resp.status_code == 200
    html = resp.data.decode('utf-8')
    # should only show 10 tickets on page 1
    assert count_list_items(html) == 10

def test_page_2_shows_next_10(client, admin_user, many_tickets):
    login(client, admin_user.username, 'adminpass')
    resp = client.get('/tickets/?page=2')
    assert resp.status_code == 200
    html = resp.data.decode('utf-8')
    # still full 10 tickets on page 2
    assert count_list_items(html) == 10

def test_last_page_shows_remainder(client, admin_user, many_tickets):
    login(client, admin_user.username, 'adminpass')
    resp = client.get('/tickets/?page=3')
    assert resp.status_code == 200
    html = resp.data.decode('utf-8')
    # only 25 total → page 3 should have 5 left
    assert count_list_items(html) == 5
