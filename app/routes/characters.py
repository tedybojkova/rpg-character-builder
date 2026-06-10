import logging
from flask import Blueprint, jsonify, request

from ..services.character_service import CharacterService
from ..services.dice_roller import DiceRoller
from ..exceptions import RPGBaseException

logger = logging.getLogger(__name__)

characters_bp = Blueprint("characters", __name__)

_service = CharacterService()
_dice_roller = DiceRoller()


@characters_bp.route("/", methods=["GET"])
def list_characters():
    characters = _service.get_all()
    return jsonify([c.to_dict() for c in characters])


@characters_bp.route("/roll", methods=["GET"])
def roll_stats():
    rolls = _dice_roller.roll_stat_array()
    stat_names = ["strength", "dexterity", "constitution",
                  "intelligence", "wisdom", "charisma"]
    result = dict(zip(stat_names, rolls))
    logger.info("Rolled stats: %s", result)
    return jsonify(result)


@characters_bp.route("/", methods=["POST"])
def create_character():
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
    try:
        character = _service.get_by_id(character_id)
        return jsonify(character.to_dict()), 200
    except RPGBaseException as e:
        return jsonify({"error": str(e)}), 404


@characters_bp.route("/<int:character_id>", methods=["PUT"])
def update_character(character_id: int):
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
    try:
        _service.delete(character_id)
        return jsonify({"message": f"Character {character_id} deleted."}), 200
    except RPGBaseException as e:
        return jsonify({"error": str(e)}), 404