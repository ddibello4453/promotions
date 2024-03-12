######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Product Promotion Service

This service implements a REST API that allows you to Create, Read, Update
and Delete Promotions from the inventory of promotions
"""

from flask import jsonify, request, url_for, abort
from flask import current_app as app  # Import Flask application
from service.models import Promotions
from service.common import status  # HTTP Status Codes


######################################################################
# GET HEALTH CHECK
######################################################################
@app.route("/health")
def health_check():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="Healthy"), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


######################################################################
# CREATE A NEW PROMOTION
######################################################################
@app.route("/promotions", methods=["POST"])
def create_promotions():
    """
    Creates a Promotion

    This endpoint will create a Promotion based the data in the body that is posted
    """
    app.logger.info("Request to create a promotion")
    check_content_type("application/json")

    promotions = Promotions()
    promotions.deserialize(request.get_json())
    promotions.create()
    message = promotions.serialize()
    location_url = url_for(
        "get_promotions", promo_id=promotions.promo_id, _external=True
    )

    app.logger.info("Promotions with ID: %d created.", promotions.promo_id)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# LIST ALL PROMOTIONS
######################################################################
@app.route("/promotions", methods=["GET"])
def list_promotions():
    """Returns all of the Promotions"""
    app.logger.info("Request for promotion list")

    promotions = []

    # See if any query filters were passed in
    category = request.args.get("category")
    name = request.args.get("name")
    if category:
        promotions = Promotions.find_by_category(category)
    elif name:
        promotions = Promotions.find_by_name(name)
    else:
        promotions = Promotions.all()

    results = [promotion.serialize() for promotion in promotions]
    app.logger.info("Returning %d promotions", len(results))
    return jsonify(results), status.HTTP_200_OK


######################################################################
# READ A PROMOTION
######################################################################
@app.route("/promotions/<int:promo_id>", methods=["GET"])
def get_promotions(promo_id):
    """
    Retrieve a single Promotion

    This endpoint will return a Promotion based on it's id
    """
    app.logger.info("Request for promotion with id: %s", promo_id)

    promotion = Promotions.find(promo_id)
    if not promotion:
        error(
            status.HTTP_404_NOT_FOUND,
            f"Promotion with id '{promo_id}' was not found.",
        )

    app.logger.info("Returning promotion: %s", promotion.promo_id)
    return jsonify(promotion.serialize()), status.HTTP_200_OK


######################################################################
# DELETE A Promotion
######################################################################
@app.route("/promotions/<int:promo_id>", methods=["DELETE"])
def delete_promotion(promo_id):
    """
    Delete a Promotion

    This endpoint will delete a Promo based the id specified in the path
    """
    app.logger.info("Request to delete promo with id: %d", promo_id)

    promotion = Promotions.find(promo_id)
    if promotion:
        promotion.delete()

    app.logger.info("Promotion with ID: %d delete complete.", promo_id)
    return "", status.HTTP_204_NO_CONTENT


######################################################################
# Update a promotion
######################################################################


@app.route("/promotions/<int:promo_id>", methods=["PUT"])
def update_promotions(promo_id):
    """
    Update a Promotion

    This endpoint will update a Promotion based the body that is posted
    """
    app.logger.info("Request to update promotion with id: %d", promo_id)
    check_content_type("application/json")

    promotion = Promotions.find(promo_id)
    if not promotion:
        error(
            status.HTTP_404_NOT_FOUND,
            f"Promotion with id: '{promo_id}' was not found.",
        )

    promotion.deserialize(request.get_json())
    promotion.promo_id = promo_id
    promotion.update()

    app.logger.info("Promotion with ID: %d updated.", promotion.promo_id)
    return jsonify(promotion.serialize()), status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


######################################################################
# Checks the ContentType of a request
######################################################################
def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        error(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    error(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )


######################################################################
# Logs error messages before aborting
######################################################################
def error(status_code, reason):
    """Logs the error and then aborts"""
    app.logger.error(reason)
    abort(status_code, reason)
