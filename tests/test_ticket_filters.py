def login(client, identifier, password):
    return client.post(
        '/login',
        data={'identifier': identifier, 'password': password},
        follow_redirects=True
    )

def test_filter_status_no_match(client, admin_user):
    login(client, admin_user.username, 'adminpass')
    resp = client.get('/tickets/?status=NonexistentStatus')
    assert resp.status_code == 200
    assert b"No tickets found" in resp.data or b"<li>" not in resp.data

def test_filter_assignee_no_match(client, admin_user):
    login(client, admin_user.username, 'adminpass')
    resp = client.get('/tickets/?assignee=99999')
    assert resp.status_code == 200
    assert b"No tickets found" in resp.data or b"<li>" not in resp.data

def test_filter_empty_result_both(client, admin_user):
    login(client, admin_user.username, 'adminpass')
    resp = client.get('/tickets/?status=Closed&assignee=99999')
    assert resp.status_code == 200
    assert b"No tickets found" in resp.data or b"<li>" not in resp.data
