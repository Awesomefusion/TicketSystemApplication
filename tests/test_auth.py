def test_login_page_loads(client):
    """The login page should return 200 and contain the text 'Login'."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data


def test_valid_login_redirects(client, admin_user):
    """Valid admin credentials should redirect to the tickets list."""
    response = client.post(
        '/login',
        data={'identifier': admin_user.username, 'password': 'adminpass'},
        follow_redirects=False
    )
    assert response.status_code == 302
    assert '/tickets/' in response.headers['Location']


def test_invalid_login_shows_error(client):
    """Invalid credentials should re-render login with an error message."""
    response = client.post(
        '/login',
        data={'identifier': 'doesnotexist', 'password': 'wrongpass'},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Invalid credentials" in response.data

def login(client, identifier, password):
    return client.post(
        '/login',
        data={'identifier': identifier, 'password': password},
        follow_redirects=True
    )

def test_logout_and_protect_routes(client, normal_user):
    # Log in as normal_user
    login(client, normal_user.username, 'userpass')

    # Log out
    resp = client.get('/logout', follow_redirects=True)
    assert resp.status_code == 200
    # After logout we should see the login page
    assert b"<h2>Login</h2>" in resp.data

    # Try accessing a protected page
    resp2 = client.get('/tickets/', follow_redirects=False)
    assert resp2.status_code == 302
    assert '/login?next=' in resp2.headers['Location']
