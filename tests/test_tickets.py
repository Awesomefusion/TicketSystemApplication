import pytest
from app import db
from app.models import Ticket


def login(client, identifier, password):
    return client.post(
        '/login',
        data={'identifier': identifier, 'password': password},
        follow_redirects=True
    )


@pytest.fixture
def user_ticket(app, normal_user):
    """Create a ticket owned by the normal user."""
    t = Ticket(
        title="User Ticket",
        description="Owned by user",
        status="Open",
        created_by=normal_user.id,
        assigned_to=normal_user.id
    )
    db.session.add(t)
    db.session.commit()
    return t


@pytest.fixture
def admin_ticket(app, admin_user):
    """Create a ticket owned by the admin."""
    t = Ticket(
        title="Admin Ticket",
        description="Owned by admin",
        status="Open",
        created_by=admin_user.id,
        assigned_to=admin_user.id
    )
    db.session.add(t)
    db.session.commit()
    return t


def test_admin_can_list_all_tickets(client, admin_user, user_ticket, admin_ticket):
    login(client, admin_user.username, 'adminpass')
    resp = client.get('/tickets/')
    assert resp.status_code == 200
    data = resp.data
    assert b"User Ticket" in data
    assert b"Admin Ticket" in data


def test_user_sees_only_their_tickets(client, normal_user, user_ticket, admin_ticket):
    login(client, normal_user.username, 'userpass')
    resp = client.get('/tickets/')
    assert resp.status_code == 200
    data = resp.data
    assert b"User Ticket" in data
    assert b"Admin Ticket" not in data


def test_create_ticket(client, normal_user):
    login(client, normal_user.username, 'userpass')
    resp = client.post(
        '/tickets/create',
        data={
            'title': 'New Ticket',
            'description': 'Created via test',
            'status': 'Open',
            'assigned_to': str(normal_user.id)
        },
        follow_redirects=True
    )
    assert resp.status_code == 200
    assert b"Ticket created" in resp.data
    assert b"New Ticket" in resp.data
    # verify in db
    assert Ticket.query.filter_by(title="New Ticket").one()


def test_view_ticket(client, normal_user, user_ticket):
    login(client, normal_user.username, 'userpass')
    resp = client.get(f'/tickets/{user_ticket.id}')
    assert resp.status_code == 200
    assert b"Owned by user" in resp.data


def test_edit_ticket(client, normal_user, user_ticket):
    login(client, normal_user.username, 'userpass')
    resp = client.post(
        f'/tickets/{user_ticket.id}/edit',
        data={
            'title': 'Updated Title',
            'description': 'Updated desc',
            'status': 'Closed',
            'assigned_to': str(normal_user.id)
        },
        follow_redirects=True
    )
    assert resp.status_code == 200
    assert b"Ticket updated" in resp.data
    # verify change in db
    t = Ticket.query.get(user_ticket.id)
    assert t.title == "Updated Title"
    assert t.status == "Closed"


def test_delete_ticket_admin(client, admin_user, user_ticket):
    login(client, admin_user.username, 'adminpass')
    resp = client.post(
        f'/tickets/{user_ticket.id}/delete',
        follow_redirects=True
    )
    assert resp.status_code == 200
    assert b"Ticket deleted" in resp.data
    # verify it’s gone
    assert Ticket.query.get(user_ticket.id) is None


def test_delete_ticket_non_admin_forbidden(client, normal_user, admin_ticket):
    login(client, normal_user.username, 'userpass')
    resp = client.post(
        f'/tickets/{admin_ticket.id}/delete',
        follow_redirects=False
    )
    assert resp.status_code == 403
