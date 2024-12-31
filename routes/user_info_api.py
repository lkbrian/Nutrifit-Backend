from sqlite3 import IntegrityError
from flask import jsonify, make_response, request
from flask_restful import Resource
from models import UserInfo,User
from config import db
class User_Info(Resource):
  def post(self):
    data = request.json
    user_id = data.get('user_id')
    print(data)
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
      return make_response(jsonify({'msg':"user doesn't exist"}),404)
    try:
      user = UserInfo(
          goal=data['goal'],
      )
      db.session.add(user)
      db.session.commit()

      return make_response(
          jsonify({"msg": "Created succesfully"}), 201
      )
    except IntegrityError:
        db.session.rollback()
        return make_response(
            jsonify(
                {"msg": "Integrity constraint failed"}
            ),
            400,
        )

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

  def patch(self, id):
        # ensure id is provided
        if id is None:
            return make_response(jsonify({"msg": "Provide user id"}), 400)

        # check that the user is available
        user = User.query.filter_by(user_id=id).first()
        if not user:
            return make_response(jsonify({"msg": "user not found"}), 404)

        # check that the data was provided
        data = request.json
        if not data:
            return {"msg": "No Input was provided"}

        # update the necessary fields
        try:
            for field, value in data.items():
              if hasattr(user, field):
                    setattr(user, field, value)
            db.session.commit()
            return make_response(jsonify({"msg": "updating goals sucessful"}), 200)

        except IntegrityError as e:
            db.session.rollback()
            error_message = str(e.orig)
            return make_response(jsonify({"msg": f" {error_message}"}), 400)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

  def delete(self, id):
        if id is None:
            return make_response(jsonify({"msg": "Provide id"}), 400)

        # check that the user is available
        user = User.query.filter_by(user_id=id).first()
        if not user:
            return make_response(jsonify({"msg": "user not found"}), 404)

        try:
            # delete the user
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({"msg": "deleted sucessfully"}), 200)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)