import uuid

from flask.views import MethodView
from flask_smorest import Api, Blueprint, abort
from flask import Flask
from marshmallow import Schema, fields

counter = 0

app = Flask(__name__)
app.config["API_TITLE"] = "IF Systems TODO REST API"
app.config["API_VERSION"] = "v0.1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
api = Api(app)

blp = Blueprint("todo", "todo", description="Todo app")

todos = {}


class TodoSchema(Schema):
    id = fields.String(dump_only=True)
    content = fields.String(required=True)


@blp.route("/todo/<string:todo_id>")
class TodoPutDelete(MethodView):

    @blp.arguments(TodoSchema)
    def patch(self, todo, todo_id):
        try:
            todos[todo_id]["content"] = todo["content"]
            return todos[todo_id]
        except Exception:
            abort(404, message="Error! Todo probably not found!")

    def delete(self, todo_id):
        try:
            del todos[todo_id]
            return {"message": "ok"}
        except Exception:
            abort(404, message="Error! Todo probably not found!")


@blp.route("/todo")
class TodoGetPost(MethodView):

    def get(self):
        return {"todos": list(todos.values())}

    @blp.arguments(TodoSchema)
    def post(self, todo):
        todo_uuid = uuid.uuid4().hex
        todo = {"id": todo_uuid, **todo}
        todos[todo_uuid] = todo
        return todo


api.register_blueprint(blp)


