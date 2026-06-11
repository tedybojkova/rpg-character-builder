from __future__ import annotations
from .database import db


class Character(db.Model):
    """Represents a pirate character in the Grand Line world.

    Characters have a class, a race, six core stats, and computed
    properties for HP, armour class, and proficiency bonus. Each
    character also has a bounty in Berry.

    Attributes:
        id: Primary key.
        name: Character name, max 50 characters.
        level: Character level between 1 and 20.
        backstory: Optional character history text.
        bounty: The character's bounty in Berry, default 0.
        class_id: Foreign key to CharacterClass.
        race_id: Foreign key to Race.
        strength: Base strength stat.
        dexterity: Base dexterity stat.
        constitution: Base constitution stat.
        intelligence: Base intelligence stat.
        wisdom: Base wisdom stat.
        charisma: Base charisma stat.
    """

    __tablename__ = "characters"

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(50), nullable=False)
    level: int = db.Column(db.Integer, nullable=False, default=1)
    backstory: str = db.Column(db.Text, nullable=False, default="A pirate sailing the Grand Line in search of the One Piece.")
    bounty: int = db.Column(db.Integer, nullable=False, default=0)

    class_id: int = db.Column(db.Integer, nullable=False)
    race_id: int = db.Column(db.Integer, nullable=False)

    strength: int = db.Column(db.Integer, nullable=False, default=10)
    dexterity: int = db.Column(db.Integer, nullable=False, default=10)
    constitution: int = db.Column(db.Integer, nullable=False, default=10)
    intelligence: int = db.Column(db.Integer, nullable=False, default=10)
    wisdom: int = db.Column(db.Integer, nullable=False, default=10)
    charisma: int = db.Column(db.Integer, nullable=False, default=10)

    @property
    def character_class(self):
        """Retrieve the associated CharacterClass object.

        Returns:
            CharacterClass: The class linked to this character.
        """
        from .character_class import CharacterClass
        return CharacterClass.query.get(self.class_id)

    @property
    def race(self):
        """Retrieve the associated Race object.

        Returns:
            Race: The race linked to this character.
        """
        from .race import Race
        return Race.query.get(self.race_id)

    @property
    def strength_modifier(self) -> int:
        """Calculate strength modifier including race bonus.

        Returns:
            int: The strength modifier value.
        """
        return (self.strength + self.race.strength_bonus - 10) // 2

    @property
    def dexterity_modifier(self) -> int:
        """Calculate dexterity modifier including race bonus.

        Returns:
            int: The dexterity modifier value.
        """
        return (self.dexterity + self.race.dexterity_bonus - 10) // 2

    @property
    def constitution_modifier(self) -> int:
        """Calculate constitution modifier including race bonus.

        Returns:
            int: The constitution modifier value.
        """
        return (self.constitution + self.race.constitution_bonus - 10) // 2

    @property
    def intelligence_modifier(self) -> int:
        """Calculate intelligence modifier including race bonus.

        Returns:
            int: The intelligence modifier value.
        """
        return (self.intelligence + self.race.intelligence_bonus - 10) // 2

    @property
    def wisdom_modifier(self) -> int:
        """Calculate wisdom modifier including race bonus.

        Returns:
            int: The wisdom modifier value.
        """
        return (self.wisdom + self.race.wisdom_bonus - 10) // 2

    @property
    def charisma_modifier(self) -> int:
        """Calculate charisma modifier including race bonus.

        Returns:
            int: The charisma modifier value.
        """
        return (self.charisma + self.race.charisma_bonus - 10) // 2

    @property
    def max_hit_points(self) -> int:
        """Calculate maximum hit points based on class hit die, constitution, and level.

        Returns:
            int: The maximum HP value.
        """
        hp = max(1, self.character_class.hit_die + self.constitution_modifier)
        return hp * self.level

    @property
    def armour_class(self) -> int:
        """Calculate armour class as 10 plus dexterity modifier.

        Returns:
            int: The armour class value.
        """
        return 10 + self.dexterity_modifier

    @property
    def proficiency_bonus(self) -> int:
        """Calculate proficiency bonus based on character level.

        Returns:
            int: The proficiency bonus value.
        """
        return (self.level - 1) // 4 + 2

    @property
    def bounty_with_level(self) -> int:
        """Calculate total bounty including a level bonus.

        Each level above 1 adds 10% of the base bounty on top.
        A level 10 character with 1,000,000 Berry base bounty
        would have 1,900,000 Berry total.

        Returns:
            int: The total bounty including level scaling.
        """
        level_multiplier = 1 + (self.level - 1) * 0.10
        return int(self.bounty * level_multiplier)

    def to_dict(self) -> dict:
        """Serialize the character to a dictionary for API responses.

        Returns:
            dict: Full character data including stats, computed values,
                bounty, and backstory.
        """
        return {
            "id": self.id,
            "name": self.name,
            "level": self.level,
            "backstory": self.backstory,
            "bounty": self.bounty,
            "bounty_with_level": self.bounty_with_level,
            "character_class": self.character_class.name,
            "race": self.race.name,
            "stats": {
                "strength": {"base": self.strength, "total": self.strength + self.race.strength_bonus, "modifier": self.strength_modifier},
                "dexterity": {"base": self.dexterity, "total": self.dexterity + self.race.dexterity_bonus, "modifier": self.dexterity_modifier},
                "constitution": {"base": self.constitution, "total": self.constitution + self.race.constitution_bonus, "modifier": self.constitution_modifier},
                "intelligence": {"base": self.intelligence, "total": self.intelligence + self.race.intelligence_bonus, "modifier": self.intelligence_modifier},
                "wisdom": {"base": self.wisdom, "total": self.wisdom + self.race.wisdom_bonus, "modifier": self.wisdom_modifier},
                "charisma": {"base": self.charisma, "total": self.charisma + self.race.charisma_bonus, "modifier": self.charisma_modifier},
            },
            "computed": {
                "max_hit_points": self.max_hit_points,
                "armour_class": self.armour_class,
                "proficiency_bonus": self.proficiency_bonus,
            },
        }

    def __repr__(self) -> str:
        """Return a developer-friendly string representation.

        Returns:
            str: String showing character name and level.
        """
        return f"<Character {self.name} Level {self.level}>"