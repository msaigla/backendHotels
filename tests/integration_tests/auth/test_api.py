import pytest


@pytest.mark.parametrize("email, password", [
    ("test1@test.ru", "123"),
    ("test2@test.ru", "4234"),
    ("test3@test.ru", "532542"),
    ("test4@test.ru", "532452"),
    ("test5@test.ru", "253432"),
])
async def test_user(email, password, ac):
    response = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password
        }
    )
    if response.status_code == 200:
        assert response.status_code == 200
        await ac.post(
            "/auth/login",
            json={
                "email": email,
                "password": password
            }
        )
        assert response.status_code == 200
        assert ac.cookies["access_token"]
        response = await ac.post(
            "/auth/me"
        )
        assert response.status_code == 200
        assert response.json()['email'] == email
        response = await ac.delete('/auth/logout')
        assert response.status_code == 200
        # assert not ac.cookies["access_token"]
        response = await ac.post(
            "/auth/me"
        )
        assert response.status_code == 401
    else:
        pass
