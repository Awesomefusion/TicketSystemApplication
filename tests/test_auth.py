def test_login_page_loads(client):
    """The login page should return 200 and contain the text 'Login'."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data
