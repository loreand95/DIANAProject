from flask import Blueprint
from controller.SearchFullController import index, search

search_full_bp = Blueprint('search_full_bp', __name__)

search_full_bp.route('/', methods=['GET'])(index)
search_full_bp.route('/', methods=['POST'])(search)