from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200


######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((pic for pic in data if pic["id"] == id), None)
    
    if picture is None:
        abort(404)
    
    return jsonify(picture), 200



######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.get_json()  # Extract picture data from the request
    
    # Check if the picture with the same id already exists
    if any(pic["id"] == new_picture["id"] for pic in data):
        return jsonify({"Message": f"picture with id {new_picture['id']} already present"}), 302
    
    # If no duplicates, add the new picture to the data list
    data.append(new_picture)
    
    # Return the newly added picture with a 201 Created status code
    return jsonify(new_picture), 201


######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    # Extract the new picture data from the request body
    updated_picture = request.get_json()

    # Find the picture by id in the data list
    picture = next((pic for pic in data if pic["id"] == id), None)
    
    if picture is None:
        # If the picture doesn't exist, return a 404 error
        return jsonify({"message": "picture not found"}), 404

    # If picture exists, update the fields
    picture.update(updated_picture)

    # Return the updated picture with a 200 status code
    return jsonify(picture), 200


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    # Find the picture by id
    picture = next((pic for pic in data if pic["id"] == id), None)

    if picture is None:
        # If the picture is not found, return a 404 error
        return jsonify({"message": "picture not found"}), 404

    # If the picture exists, delete it
    data.remove(picture)

    # Return a 204 No Content status with an empty body
    return '', 204
