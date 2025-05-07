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
