import pytest
from app import create_app
from app.models.database import db
from app.models.character import Character
from app.models.character_class import CharacterClass
from app.models.race import Race


@pytest.fixture
def app():
    flask_app = create_app(testing=True)
    with flask_app.app_context():
        yield flask_app


@pytest.fixture
def warrior_class(app):
    return CharacterClass.query.filter_by(name="Warrior").first()


@pytest.fixture
def human_race(app):
    return Race.query.filter_by(name="Human").first()


@pytest.fixture
def sample_character(app, warrior_class, human_race):
    character = Character(
        name="Test Warrior",
        level=1,
        class_id=warrior_class.id,
        race_id=human_race.id,
        strength=16,
        dexterity=14,
        constitution=12,
        intelligence=10,
        wisdom=8,
        charisma=10,
    )
    db.session.add(character)
    db.session.commit()
    return character


class TestStatModifiers:

    def test_strength_modifier(self, sample_character):
        assert sample_character.strength_modifier == 3

    def test_dexterity_modifier(self, sample_character):
        assert sample_character.dexterity_modifier == 2

    def test_wisdom_modifier_negative(self, sample_character):
        assert sample_character.wisdom_modifier == -1

    def test_intelligence_modifier_zero(self, sample_character):
        assert sample_character.intelligence_modifier == 0


class TestMaxHitPoints:

    def test_level1_hp(self, sample_character):
        assert sample_character.max_hit_points == 11

    def test_higher_level_increases_hp(self, sample_character):
        sample_character.level = 5
        db.session.commit()
        assert sample_character.max_hit_points == 55


class TestArmourClass:

    def test_ac_equals_ten_plus_dex_mod(self, sample_character):
        expected = 10 + sample_character.dexterity_modifier
        assert sample_character.armour_class == expected


class TestProficiencyBonus:

    @pytest.mark.parametrize("level,expected", [
        (1, 2), (4, 2),
        (5, 3), (8, 3),
        (9, 4), (12, 4),
        (17, 6), (20, 6),
    ])
    def test_proficiency_bonus(self, sample_character, level, expected):
        sample_character.level = level
        assert sample_character.proficiency_bonus == expected