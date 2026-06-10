import logging
from flask import Blueprint, jsonify

from ..models.character_class import CharacterClass

logger = logging.getLogger(__name__)

classes_bp = Blueprint("classes", __name__)


@classes_bp.route("/", methods=["GET"])
def list_classes():
    classes = CharacterClass.query.all()
    logger.info("Retrieved %d classes.", len(classes))
    return jsonify([c.to_dict() for c in classes])


@classes_bp.route("/<int:class_id>", methods=["GET"])
def get_class(class_id: int):
    character_class = CharacterClass.query.get(class_id)
    if character_class is None:
        return jsonify({"error": f"Class ID {class_id} not found."}), 404
    return jsonify(character_class.to_dict()), 200