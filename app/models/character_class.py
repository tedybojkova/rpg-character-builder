from __future__ import annotations
from .database import db


class CharacterClass(db.Model):

    __tablename__ = "character_classes"

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(50), unique=True, nullable=False)
    hit_die: int = db.Column(db.Integer, nullable=False)
    primary_stat: str = db.Column(db.String(20), nullable=False)
    description: str = db.Column(db.String(500), nullable=False, default="")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "hit_die": self.hit_die,
            "primary_stat": self.primary_stat,
            "description": self.description,
        }

    def __repr__(self) -> str:
        return f"<CharacterClass {self.name} (d{self.hit_die})>"