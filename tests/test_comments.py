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
def ticket(app, admin_user):
    # Create a ticket by admin
    ticket = Ticket(
        title="Sample Ticket",
        description="Sample Description",
        status="Open",
        created_by=admin_user.id,
        assigned_to=admin_user.id
    )
    db.session.add(ticket)
    db.session.commit()
    return ticket


def test_admin_can_comment(client, admin_user, ticket):
    login(client, admin_user.username, 'adminpass')
    response = client.post(
        f'/tickets/{ticket.id}/comment',
        data={'comment': 'Admin comment'},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Comment added" in response.data
    assert b"Admin comment" in response.data


def test_ticket_creator_can_comment(client, normal_user, app):
    # Create a ticket by normal user and grab its ID within the session
    with app.app_context():
        t = Ticket(
            title="User Ticket",
            description="User description",
            status="Open",
            created_by=normal_user.id,
            assigned_to=normal_user.id
        )
        db.session.add(t)
        db.session.commit()
        ticket_id = t.id  # capture the primary key before the session closes

    login(client, normal_user.username, 'userpass')
    response = client.post(
        f'/tickets/{ticket_id}/comment',
        data={'comment': 'User comment'},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Comment added" in response.data
    assert b"User comment" in response.data


def test_normal_user_cannot_comment_others(client, normal_user, ticket):
    login(client, normal_user.username, 'userpass')
    response = client.post(
        f'/tickets/{ticket.id}/comment',
        data={'comment': 'Unauthorized comment'},
        follow_redirects=False
    )
    assert response.status_code == 403
