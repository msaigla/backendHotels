import pytest


@pytest.mark.parametrize("email, password, status_code", [
    ("test@test.ru", "123", 400),
    ("test1", "123", 422),
    ("test2@test.ru", "4234", 200),
    ("test3@test.ru", "532542", 200),
    ("test4@test.ru", "532452", 200),
    ("test5@test.ru", "253432", 200),
])
async def test_user(email: str, password: str, status_code: int, ac):
    response = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password
        }
    )
    assert response.status_code == status_code
    if status_code != 200:
        return

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
    assert "id" in response.json()
    assert "password" not in response.json()
    assert "hashed_password" not in response.json()

    response = await ac.delete('/auth/logout')
    assert response.status_code == 200
    response = await ac.post(
        "/auth/me"
    )
    assert response.status_code == 401
