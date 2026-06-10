import pytest
from app import create_app


@pytest.fixture
def client():
    flask_app = create_app(testing=True)
    with flask_app.test_client() as client:
        with flask_app.app_context():
            yield client


VALID_CHARACTER = {
    "name": "Thorin",
    "class_name": "Warrior",
    "race_name": "Dwarf",
    "level": 1,
    "strength": 16,
    "dexterity": 10,
    "constitution": 16,
    "intelligence": 8,
    "wisdom": 10,
    "charisma": 8,
}


class TestClassesEndpoint:

    def test_get_classes_returns_200(self, client):
        response = client.get("/classes/")
        assert response.status_code == 200

    def test_get_classes_returns_list(self, client):
        response = client.get("/classes/")
        data = response.get_json()
        assert isinstance(data, list)

    def test_classes_have_required_fields(self, client):
        response = client.get("/classes/")
        data = response.get_json()
        for cls in data:
            assert "name" in cls
            assert "hit_die" in cls


class TestRacesEndpoint:

    def test_get_races_returns_200(self, client):
        response = client.get("/races/")
        assert response.status_code == 200

    def test_races_have_bonuses(self, client):
        response = client.get("/races/")
        data = response.get_json()
        for race in data:
            assert "bonuses" in race


class TestCreateCharacter:

    def test_create_returns_201(self, client):
        response = client.post("/characters/", json=VALID_CHARACTER)
        assert response.status_code == 201

    def test_create_returns_correct_name(self, client):
        response = client.post("/characters/", json=VALID_CHARACTER)
        data = response.get_json()
        assert data["name"] == "Thorin"

    def test_create_has_computed_stats(self, client):
        response = client.post("/characters/", json=VALID_CHARACTER)
        data = response.get_json()
        assert "computed" in data
        assert data["computed"]["max_hit_points"] > 0

    def test_blank_name_returns_400(self, client):
        bad = {**VALID_CHARACTER, "name": ""}
        response = client.post("/characters/", json=bad)
        assert response.status_code == 400

    def test_invalid_stat_returns_400(self, client):
        bad = {**VALID_CHARACTER, "strength": 99}
        response = client.post("/characters/", json=bad)
        assert response.status_code == 400

    def test_invalid_class_returns_400(self, client):
        bad = {**VALID_CHARACTER, "class_name": "Plumber"}
        response = client.post("/characters/", json=bad)
        assert response.status_code == 400


class TestGetUpdateDelete:

    def _create(self, client):
        response = client.post("/characters/", json=VALID_CHARACTER)
        return response.get_json()["id"]

    def test_get_character_by_id(self, client):
        char_id = self._create(client)
        response = client.get(f"/characters/{char_id}")
        assert response.status_code == 200

    def test_get_wrong_id_returns_404(self, client):
        response = client.get("/characters/99999")
        assert response.status_code == 404

    def test_update_character_name(self, client):
        char_id = self._create(client)
        response = client.put(
            f"/characters/{char_id}",
            json={"name": "Thorin Oakenshield"}
        )
        assert response.status_code == 200
        assert response.get_json()["name"] == "Thorin Oakenshield"

    def test_delete_character(self, client):
        char_id = self._create(client)
        delete = client.delete(f"/characters/{char_id}")
        assert delete.status_code == 200
        get = client.get(f"/characters/{char_id}")
        assert get.status_code == 404


class TestRollStats:

    def test_roll_returns_six_stats(self, client):
        response = client.get("/characters/roll")
        data = response.get_json()
        expected = {"strength", "dexterity", "constitution",
                    "intelligence", "wisdom", "charisma"}
        assert set(data.keys()) == expected

    def test_rolled_stats_in_valid_range(self, client):
        for _ in range(5):
            response = client.get("/characters/roll")
            data = response.get_json()
            for stat, value in data.items():
                assert 3 <= value <= 18