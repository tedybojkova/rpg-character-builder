from __future__ import annotations
from .database import db


class Race(db.Model):

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
            }
        }

    def __repr__(self) -> str:
        return f"<Race {self.name}>"