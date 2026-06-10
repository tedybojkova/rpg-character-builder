from __future__ import annotations
from .database import db


class Character(db.Model):

    __tablename__ = "characters"

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(50), nullable=False)
    level: int = db.Column(db.Integer, nullable=False, default=1)
    backstory: str = db.Column(db.Text, nullable=False, default="")

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
        from .character_class import CharacterClass
        return CharacterClass.query.get(self.class_id)

    @property
    def race(self):
        from .race import Race
        return Race.query.get(self.race_id)

    @property
    def strength_modifier(self) -> int:
        total = self.strength + self.race.strength_bonus
        return (total - 10) // 2

    @property
    def dexterity_modifier(self) -> int:
        total = self.dexterity + self.race.dexterity_bonus
        return (total - 10) // 2

    @property
    def constitution_modifier(self) -> int:
        total = self.constitution + self.race.constitution_bonus
        return (total - 10) // 2

    @property
    def intelligence_modifier(self) -> int:
        total = self.intelligence + self.race.intelligence_bonus
        return (total - 10) // 2

    @property
    def wisdom_modifier(self) -> int:
        total = self.wisdom + self.race.wisdom_bonus
        return (total - 10) // 2

    @property
    def charisma_modifier(self) -> int:
        total = self.charisma + self.race.charisma_bonus
        return (total - 10) // 2

    @property
    def max_hit_points(self) -> int:
        hp = max(1, self.character_class.hit_die + self.constitution_modifier)
        return hp * self.level

    @property
    def armour_class(self) -> int:
        return 10 + self.dexterity_modifier

    @property
    def proficiency_bonus(self) -> int:
        return (self.level - 1) // 4 + 2

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "level": self.level,
            "backstory": self.backstory,
            "character_class": self.character_class.name,
            "race": self.race.name,
            "stats": {
                "strength":     {"base": self.strength,     "modifier": self.strength_modifier},
                "dexterity":    {"base": self.dexterity,    "modifier": self.dexterity_modifier},
                "constitution": {"base": self.constitution, "modifier": self.constitution_modifier},
                "intelligence": {"base": self.intelligence, "modifier": self.intelligence_modifier},
                "wisdom":       {"base": self.wisdom,       "modifier": self.wisdom_modifier},
                "charisma":     {"base": self.charisma,     "modifier": self.charisma_modifier},
            },
            "computed": {
                "max_hit_points": self.max_hit_points,
                "armour_class": self.armour_class,
                "proficiency_bonus": self.proficiency_bonus,
            }
        }

    def __repr__(self) -> str:
        return f"<Character {self.name} Level {self.level}>"