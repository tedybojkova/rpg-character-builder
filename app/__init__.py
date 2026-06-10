import logging as log
from flask import Flask
from .models.database import db
from .logging_config import setup_logging


def create_app(testing: bool = False) -> Flask:
    app = Flask(__name__)

    if testing:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["TESTING"] = True
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///rpg.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    setup_logging()
    logger = log.getLogger(__name__)
    logger.info("Starting RPG Character Builder...")

    db.init_app(app)

    from .routes.characters import characters_bp
    from .routes.classes import classes_bp
    from .routes.races import races_bp

    app.register_blueprint(characters_bp, url_prefix="/characters")
    app.register_blueprint(classes_bp, url_prefix="/classes")
    app.register_blueprint(races_bp, url_prefix="/races")

    with app.app_context():
        from .models.character_class import CharacterClass
        from .models.race import Race
        from .models.character import Character
        db.create_all()
        _seed_data()

    return app


def _seed_data() -> None:
    from .models.character_class import CharacterClass
    from .models.race import Race

    if CharacterClass.query.count() == 0:
        classes = [
            CharacterClass(name="Warrior",  hit_die=10, primary_stat="strength",     description="A master of martial combat."),
            CharacterClass(name="Mage",     hit_die=6,  primary_stat="intelligence", description="A scholarly magic user."),
            CharacterClass(name="Rogue",    hit_die=8,  primary_stat="dexterity",    description="A scoundrel who uses stealth."),
            CharacterClass(name="Cleric",   hit_die=8,  primary_stat="wisdom",       description="A divine magic wielder."),
            CharacterClass(name="Ranger",   hit_die=10, primary_stat="dexterity",    description="A warrior of the wilderness."),
            CharacterClass(name="Bard",     hit_die=8,  primary_stat="charisma",     description="An inspiring magician."),
        ]
        db.session.add_all(classes)

    if Race.query.count() == 0:
        races = [
            Race(name="Human",    description="Versatile and ambitious.",          strength_bonus=1, dexterity_bonus=1, constitution_bonus=1, intelligence_bonus=1, wisdom_bonus=1, charisma_bonus=1),
            Race(name="Elf",      description="Ancient and graceful.",             dexterity_bonus=2, intelligence_bonus=1),
            Race(name="Dwarf",    description="Stout and sturdy.",                 constitution_bonus=2, wisdom_bonus=1),
            Race(name="Halfling", description="Small but brave.",                  dexterity_bonus=2, charisma_bonus=1),
            Race(name="Orc",      description="Powerful and fierce.",              strength_bonus=2, constitution_bonus=2, charisma_bonus=-2),
            Race(name="Gnome",    description="Curious and inventive.",            intelligence_bonus=2),
        ]
        db.session.add_all(races)

    db.session.commit()