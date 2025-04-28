async def test_add_facilities(ac):
    facility_title = "TV"
    response = await ac.post(
        "/facilities",
        json={
            "title": facility_title
        }
    )
    assert response.status_code == 200
    res = response.json()
    assert isinstance(response.json(), dict)
    assert res["data"]['title'] == facility_title
    assert "data" in res



async def test_get_facilities(ac):
    response = await ac.get("/facilities")
    assert response.status_code == 200
    isinstance(response.json(), list)
