import logging as log
from flask import Flask
from .models.database import db
from .logging_config import setup_logging


def create_app(testing: bool = False) -> Flask:
    """Create and configure the Flask application.

    Sets up the database, logging, blueprints, and seeds initial data
    when running for the first time.

    Args:
        testing: If True, uses an in-memory SQLite database.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)

    if testing:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["TESTING"] = True
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///rpg.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    setup_logging()
    logger = log.getLogger(__name__)
    logger.info("Setting sail on the Grand Line...")

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
    """Seed the database with initial One Piece classes and races.

    Only inserts data if the tables are empty, so it is safe to call
    on every app startup without creating duplicates.
    """
    from .models.character_class import CharacterClass
    from .models.race import Race
    from .models.database import db

    if CharacterClass.query.count() == 0:
        classes = [
            CharacterClass(name="Swordsman", hit_die=10, primary_stat="strength", description="A master of blade combat who fights with power and precision, like the Pirate Hunter Zoro."),
            CharacterClass(name="Navigator", hit_die=6, primary_stat="intelligence", description="A tactical genius who uses knowledge and weather to outsmart any enemy, like the Cat Burglar Nami."),
            CharacterClass(name="Sniper", hit_die=8, primary_stat="dexterity", description="A long-range specialist with incredible aim and resourcefulness, like the King of Snipers Usopp."),
            CharacterClass(name="Cook", hit_die=8, primary_stat="dexterity", description="A powerful fighter who uses only their legs in combat and never wastes their hands, like the Black Leg Sanji."),
            CharacterClass(name="Doctor", hit_die=8, primary_stat="wisdom", description="A brilliant medic who can heal any wound and fight with surprising strength, like the Cotton Candy Lover Chopper."),
            CharacterClass(name="Devil Fruit User", hit_die=6, primary_stat="charisma", description="A fighter with an unpredictable and powerful Devil Fruit ability, like the Straw Hat Luffy."),
            CharacterClass(name="Shipwright", hit_die=10, primary_stat="constitution", description="A powerhouse builder and fighter with a cyborg body, like the Cyborg Franky."),
            CharacterClass(name="Musician", hit_die=6, primary_stat="charisma", description="A soulful fighter who returns from death itself to keep the crews spirits high, like Soul King Brook."),
            CharacterClass(name="Archaeologist", hit_die=6, primary_stat="intelligence", description="A genius scholar who can sprout arms from any surface to overwhelm enemies, like the Demon Child Robin."),
            CharacterClass(name="Pirate Captain", hit_die=8, primary_stat="charisma", description="A bold and inspiring leader who rallies their crew through impossible odds."),
            CharacterClass(name="Marine", hit_die=10, primary_stat="strength", description="A disciplined enforcer of justice who fights for the World Government."),
            CharacterClass(name="Bounty Hunter", hit_die=10, primary_stat="dexterity", description="A ruthless tracker who hunts pirates for fame and fortune across the seas."),
        ]
        db.session.add_all(classes)

    if Race.query.count() == 0:
        races = [
            Race(name="Human", description="The most common race in the One Piece world. Versatile and found on every sea.", strength_bonus=1, dexterity_bonus=1, constitution_bonus=1, intelligence_bonus=1, wisdom_bonus=1, charisma_bonus=1),
            Race(name="Fishman", description="Powerful aquatic warriors with incredible physical strength. Ten times stronger than humans.", strength_bonus=2, constitution_bonus=2),
            Race(name="Giant", description="Massive warriors from Elbaf with overwhelming strength and endurance.", strength_bonus=3, constitution_bonus=2, charisma_bonus=-1),
            Race(name="Mink", description="Animal-human hybrids from Zou who can use Electro and are strongest at night.", dexterity_bonus=2, wisdom_bonus=1),
            Race(name="Cyborg", description="Humans enhanced with scientific modifications for incredible durability, like Franky.", constitution_bonus=3, intelligence_bonus=1, charisma_bonus=-2),
            Race(name="Lunarian", description="A nearly extinct race from the Red Line with incredible resilience and fire abilities.", strength_bonus=1, dexterity_bonus=1, constitution_bonus=3),
            Race(name="Longarm Tribe", description="A tribe with double-jointed arms giving them extraordinary reach and dexterity.", dexterity_bonus=3, intelligence_bonus=1),
            Race(name="Longleg Tribe", description="A tribe with incredibly long legs giving them powerful kicks and swift movement.", dexterity_bonus=2, strength_bonus=1),
            Race(name="Tontatta", description="Tiny but fierce dwarves from Green Bit with superhuman speed and a strong sense of justice.", dexterity_bonus=3, wisdom_bonus=1, strength_bonus=-1),
            Race(name="Skypiean", description="Winged inhabitants of Skypiea with deep wisdom and knowledge of the ancient world.", wisdom_bonus=2, dexterity_bonus=1),
        ]
        db.session.add_all(races)

    db.session.commit()