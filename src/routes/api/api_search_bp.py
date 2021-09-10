from flask import Blueprint
from controller.SearchController import search
from controller.api.SearchControllerApi import index, store, table

api_search_bp = Blueprint('api_search_bp', __name__)

api_search_bp.route('/', methods=['GET'])(index)
api_search_bp.route('/', methods=['POST'])(store)
api_search_bp.route('/table', methods=['POST'])(table)