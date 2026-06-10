from __future__ import annotations
from .database import db


class CharacterClass(db.Model):
    """Represents a playable character class in the Grand Line world.

    Each class defines the type of fighter a character is, their hit die
    for HP calculation, and their primary stat focus.

    Attributes:
        id: Primary key.
        name: Unique class name (e.g. Swordsman, Navigator).
        hit_die: The die used to calculate max HP (e.g. 10 for d10).
        primary_stat: The main stat this class relies on.
        description: Flavour text describing the class.
    """

    __tablename__ = "character_classes"

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(50), unique=True, nullable=False)
    hit_die: int = db.Column(db.Integer, nullable=False)
    primary_stat: str = db.Column(db.String(20), nullable=False)
    description: str = db.Column(db.String(500), nullable=False, default="")

    def to_dict(self) -> dict:
        """Serialize the character class to a dictionary for API responses.

        Returns:
            dict: A dictionary containing id, name, hit_die, primary_stat,
                and description.
        """
        return {
            "id": self.id,
            "name": self.name,
            "hit_die": self.hit_die,
            "primary_stat": self.primary_stat,
            "description": self.description,
        }

    def __repr__(self) -> str:
        """Return a developer-friendly string representation.

        Returns:
            str: String showing class name and hit die.
        """
        return f"<CharacterClass {self.name} (d{self.hit_die})>"