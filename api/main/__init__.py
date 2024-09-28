from flask import Blueprint

main = Blueprint("main", __name__, "")

# Import here to avoid circular dependencies
from . import endpoints
