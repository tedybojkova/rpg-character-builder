import logging
from flask import Blueprint, jsonify

from ..models.race import Race

logger = logging.getLogger(__name__)

races_bp = Blueprint("races", __name__)


@races_bp.route("/", methods=["GET"])
def list_races():
    races = Race.query.all()
    logger.info("Retrieved %d races.", len(races))
    return jsonify([r.to_dict() for r in races])


@races_bp.route("/<int:race_id>", methods=["GET"])
def get_race(race_id: int):
    race = Race.query.get(race_id)
    if race is None:
        return jsonify({"error": f"Race ID {race_id} not found."}), 404
    return jsonify(race.to_dict()), 200