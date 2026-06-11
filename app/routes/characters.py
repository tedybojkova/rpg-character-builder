"""Flask blueprint for character endpoints."""
import logging
from flask import Blueprint, jsonify, request

from ..services.character_service import CharacterService
from ..services.dice_roller import DiceRoller
from ..exceptions import RPGBaseException

logger = logging.getLogger(__name__)

characters_bp = Blueprint(name="characters", import_name=__name__)

_service = CharacterService()
_dice_roller = DiceRoller()


@characters_bp.route("/", methods=["GET"])
def list_characters():
    """Return a list of all characters in the database.

    Returns:
        JSON list of all characters with their full stats.
    """
    characters = _service.get_all()
    return jsonify([c.to_dict() for c in characters])


@characters_bp.route("/roll", methods=["GET"])
def roll_stats():
    """Roll a random set of six stats for character creation.

    Returns:
        JSON dict mapping each stat name to a rolled value
        between 3 and 18.Only for
    """
    rolls = _dice_roller.roll_stat_array()
    stat_names = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
    result = dict(zip(stat_names, rolls))
    logger.info("Rolled stats: %s", result)
    return jsonify(result)


@characters_bp.route("/", methods=["POST"])
def create_character():
    """Create a new character from JSON request data.

    Expected JSON fields:
        name: Character name (required).
        class_name: Name of the character class (required).
        race_name: Name of the race (required).
        level: Character level 1-20 (optional, default 1).
        backstory: Character backstory (optional).
        bounty: Starting bounty in Berry (optional, default 0).
        strength, dexterity, constitution,
        intelligence, wisdom, charisma: Stats 1-20 (optional).

    Returns:
        JSON of the created character with status 201,
        or error message with status 400.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400
    try:
        character = _service.create(data)
        return jsonify(character.to_dict()), 201
    except RPGBaseException as e:
        return jsonify({"error": str(e)}), 400


@characters_bp.route("/<int:character_id>", methods=["GET"])
def get_character(character_id: int):
    """Return a single character by ID.

    Args:
        character_id: The ID of the character to retrieve.

    Returns:
        JSON of the character, or 404 error if not found.
    """
    try:
        character = _service.get_by_id(character_id)
        return jsonify(character.to_dict()), 200
    except RPGBaseException as e:
        return jsonify({"error": str(e)}), 404


@characters_bp.route("/<int:character_id>", methods=["PUT"])
def update_character(character_id: int):
    """Update an existing character by ID.

    Args:
        character_id: The ID of the character to update.

    Returns:
        JSON of the updated character, or error with status 400.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400
    try:
        character = _service.update(character_id, data)
        return jsonify(character.to_dict()), 200
    except RPGBaseException as e:
        return jsonify({"error": str(e)}), 400


@characters_bp.route("/<int:character_id>", methods=["DELETE"])
def delete_character(character_id: int):
    """Delete a character by ID.

    Args:
        character_id: The ID of the character to delete.

    Returns:
        JSON success message, or 404 error if not found.
    """
    try:
        _service.delete(character_id)
        return jsonify({"message": f"Character {character_id} deleted."}), 200
    except RPGBaseException as e:
        return jsonify({"error": str(e)}), 404