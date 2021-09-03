from flask import Blueprint
from controller.SearchController import index, search

search_bp = Blueprint('search_bp', __name__)

search_bp.route('/', methods=['GET'])(index)
search_bp.route('/', methods=['POST'])(search)