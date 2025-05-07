import pytest
from app import db
from app.models import Ticket

def login(client, identifier, password):
    return client.post(
        '/login',
        data={'identifier': identifier, 'password': password},
        follow_redirects=True
    )

def test_404_page(client):
    """Requesting a non-existent page returns 404 with the correct template."""
    response = client.get('/no-such-page')
    assert response.status_code == 404
    assert b"404 Not Found" in response.data

def test_403_page(client, normal_user, admin_user, app):
    """
    A normal user attempting to view another user's ticket
    should get a 403 Forbidden with the custom template.
    """
    # Seed a ticket owned by admin
    with app.app_context():
        t = Ticket(
            title="Hidden Ticket",
            description="You shall not pass",
            status="Open",
            created_by=admin_user.id,
            assigned_to=admin_user.id
        )
        db.session.add(t)
        db.session.commit()
        ticket_id = t.id

    # Log in as normal_user
    login(client, normal_user.username, 'userpass')

    # Attempt to view admin's ticket
    response = client.get(f'/tickets/{ticket_id}', follow_redirects=True)
    assert response.status_code == 403
    assert b"403 Forbidden" in response.data
