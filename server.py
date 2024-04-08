from typing import Type
import flask
from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_bcrypt import Bcrypt
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from models import Session, User, Advertisement
from schema import CreateUser, UpdateUser, CreateAdvertisement, UpdateAdvertisement

app = Flask("app")
bcrypt = Bcrypt(app)


def hash_password(password: str) -> str:
    password = password.encode()
    return bcrypt.generate_password_hash(password).decode()


def check_password(password: str, hashed: str) -> bool:
    password = password.encode()
    hashed = hashed.encode()
    return bcrypt.check_password_hash(hashed, password)


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response: flask.Response):
    request.session.close()
    return response


class HttpError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"error": error.message})
    response.status_code = error.status_code
    return response


def get_user_by_id(user_id: int):
    user = request.session.query(User).get(user_id)
    if user is None:
        raise HttpError(404, "user not found")
    return user


def get_advertisement_by_id(adv_id: int):
    advertisement = request.session.query(Advertisement).get(adv_id)
    if advertisement is None:
        raise HttpError(404, "advertisement not found")
    return advertisement


def add_user(user: User):
    try:
        request.session.add(user)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "user already exists")


def add_advertisement(adv: Advertisement):
    try:
        request.session.add(adv)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "no such user exists")


def validate_json(
        json_data: dict,
        schema_class: Type[CreateUser] | Type[UpdateUser] | Type[CreateAdvertisement] | Type[UpdateAdvertisement]
):
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except ValidationError as er:
        error = er.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)


class UserView(MethodView):
    def get(self, user_id: int):
        user = get_user_by_id(user_id)
        return jsonify(user.dict)

    def post(self):
        user_data = validate_json(request.json, CreateUser)
        user = User(**user_data)
        add_user(user)
        return jsonify(user.dict)

    def patch(self, user_id: int):
        user_data = validate_json(request.json, UpdateUser)
        user = get_user_by_id(user_id)
        for field, value in user_data.items():
            setattr(user, field, value)
        add_user(user)
        return jsonify(user.dict)

    def delete(self, user_id: int):
        user = get_user_by_id(user_id)
        request.session.delete(user)
        request.session.commit()
        return jsonify({"status": "deleted"})


class AdvertisementView(MethodView):
    def get(self, adv_id: int):
        advertisement = get_advertisement_by_id(adv_id)
        return jsonify(advertisement.dict)

    def post(self):
        adv_data = validate_json(request.json, CreateAdvertisement)
        advertisement = Advertisement(**adv_data)
        add_advertisement(advertisement)
        return jsonify(advertisement.dict)

    def patch(self, adv_id: int):
        adv_data = validate_json(request.json, UpdateAdvertisement)
        adv = get_advertisement_by_id(adv_id)
        for field, value in adv_data.items():
            setattr(adv, field, value)
        add_user(adv)
        return jsonify(adv.dict)

    def delete(self, adv_id: int):
        adv = get_advertisement_by_id(adv_id)
        request.session.delete(adv)
        request.session.commit()
        return jsonify({"status": "deleted"})


user_view = UserView.as_view("user_view")
advertisement_view = AdvertisementView.as_view("advertisement_view")

app.add_url_rule("/user/<int:user_id>",
                 view_func=user_view,
                 methods=["GET", "PATCH", "DELETE"])

app.add_url_rule("/user",
                 view_func=user_view,
                 methods=["POST"])

app.add_url_rule("/advertisement/<int:adv_id>",
                 view_func=advertisement_view,
                 methods=["GET", "PATCH", "DELETE"])

app.add_url_rule("/advertisement",
                 view_func=advertisement_view,
                 methods=["POST"])


if __name__ == "__main__":
    app.run()
