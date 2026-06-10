from __future__ import annotations
from .database import db


class Race(db.Model):
    """Represents a playable race in the Grand Line world.

    Each race provides stat bonuses that are applied on top of a
    character's base stats when calculating modifiers.

    Attributes:
        id: Primary key.
        name: Unique race name (e.g. Human, Fishman, Giant).
        description: Flavour text describing the race.
        strength_bonus: Bonus added to strength stat.
        dexterity_bonus: Bonus added to dexterity stat.
        constitution_bonus: Bonus added to constitution stat.
        intelligence_bonus: Bonus added to intelligence stat.
        wisdom_bonus: Bonus added to wisdom stat.
        charisma_bonus: Bonus added to charisma stat.
    """

    __tablename__ = "Races"

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(50), unique=True, nullable=False)
    description: str = db.Column(db.String(500), nullable=False, default="")
    strength_bonus: int = db.Column(db.Integer, default=0)
    dexterity_bonus: int = db.Column(db.Integer, default=0)
    constitution_bonus: int = db.Column(db.Integer, default=0)
    intelligence_bonus: int = db.Column(db.Integer, default=0)
    wisdom_bonus: int = db.Column(db.Integer, default=0)
    charisma_bonus: int = db.Column(db.Integer, default=0)

    def to_dict(self) -> dict:
        """Serialize the race to a dictionary for API responses.

        Returns:
            dict: A dictionary containing id, name, description,
                and a nested bonuses dict with all stat bonuses.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "bonuses": {
                "strength": self.strength_bonus,
                "dexterity": self.dexterity_bonus,
                "constitution": self.constitution_bonus,
                "intelligence": self.intelligence_bonus,
                "wisdom": self.wisdom_bonus,
                "charisma": self.charisma_bonus,
            },
        }

    def __repr__(self) -> str:
        """Return a developer-friendly string representation.

        Returns:
            str: String showing the race name.
        """
        return f"<Race {self.name}>"