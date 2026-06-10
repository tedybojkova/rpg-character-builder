import logging
from typing import List

from ..models.database import db
from ..models.character import Character
from ..models.character_class import CharacterClass
from ..models.race import Race
from ..exceptions import (
    CharacterNotFoundException,
    ClassNotFoundException,
    RaceNotFoundException,
    InvalidStatValueError,
    InvalidCharacterNameError,
    InvalidLevelError,
)

logger = logging.getLogger(__name__)

MIN_STAT = 1
MAX_STAT = 20
MIN_LEVEL = 1
MAX_LEVEL = 20
MAX_NAME_LENGTH = 50


class CharacterService:

    def get_all(self) -> List[Character]:
        characters = Character.query.all()
        logger.info("Retrieved %d characters.", len(characters))
        return characters

    def get_by_id(self, character_id: int) -> Character:
        character = Character.query.get(character_id)
        if character is None:
            logger.warning("Character ID %d not found.", character_id)
            raise CharacterNotFoundException(character_id)
        return character

    def create(self, data: dict) -> Character:
        logger.info("Creating character: %s", data)

        name = data.get("name", "").strip()
        self._validate_name(name)

        level = int(data.get("level", 1))
        self._validate_level(level)

        class_name = data.get("class_name", "")
        character_class = CharacterClass.query.filter_by(name=class_name).first()
        if character_class is None:
            raise ClassNotFoundException(class_name)

        race_name = data.get("race_name", "")
        race = Race.query.filter_by(name=race_name).first()
        if race is None:
            raise RaceNotFoundException(race_name)

        stat_names = ["strength", "dexterity", "constitution",
                      "intelligence", "wisdom", "charisma"]
        stats = {}
        for stat in stat_names:
            value = int(data.get(stat, 10))
            self._validate_stat(stat, value)
            stats[stat] = value

        character = Character(
            name=name,
            level=level,
            class_id=character_class.id,
            race_id=race.id,
            backstory=data.get("backstory", ""),
            **stats,
        )
        db.session.add(character)
        db.session.commit()

        logger.info("Character created: %s (ID=%d)", character.name, character.id)
        return character

    def update(self, character_id: int, data: dict) -> Character:
        character = self.get_by_id(character_id)

        if "name" in data:
            self._validate_name(data["name"].strip())
            character.name = data["name"].strip()

        if "level" in data:
            self._validate_level(int(data["level"]))
            character.level = int(data["level"])

        if "backstory" in data:
            character.backstory = data["backstory"]

        for stat in ["strength", "dexterity", "constitution",
                     "intelligence", "wisdom", "charisma"]:
            if stat in data:
                value = int(data[stat])
                self._validate_stat(stat, value)
                setattr(character, stat, value)

        db.session.commit()
        logger.info("Character ID %d updated.", character_id)
        return character

    def delete(self, character_id: int) -> None:
        character = self.get_by_id(character_id)
        db.session.delete(character)
        db.session.commit()
        logger.info("Character ID %d deleted.", character_id)

    def _validate_name(self, name: str) -> None:
        if not name or len(name) > MAX_NAME_LENGTH:
            raise InvalidCharacterNameError(name)

    def _validate_stat(self, stat_name: str, value: int) -> None:
        if not MIN_STAT <= value <= MAX_STAT:
            raise InvalidStatValueError(stat_name, value)

    def _validate_level(self, level: int) -> None:
        if not MIN_LEVEL <= level <= MAX_LEVEL:
            raise InvalidLevelError(level)