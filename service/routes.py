"""
Account Service

This microservice handles the lifecycle of Accounts
"""
# pylint: disable=unused-import
from flask import jsonify, request, make_response, abort, url_for   # noqa; F401
from service.models import Account
from service.common import status  # HTTP Status Codes
from . import app  # Import Flask application


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Account REST API Service",
            version="1.0",
            # paths=url_for("list_accounts", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
# CREATE A NEW ACCOUNT
######################################################################
@app.route("/accounts", methods=["POST"])
def create_accounts():
    """
    Creates an Account
    This endpoint will create an Account based the data in the body that is posted
    """
    app.logger.info("Request to create an Account")
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    message = account.serialize()
    # Uncomment once get_accounts has been implemented
    # location_url = url_for("get_accounts", account_id=account.id, _external=True)
    location_url = "/"  # Remove once get_accounts has been implemented
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# LIST ALL ACCOUNTS
######################################################################

# ... place you code here to LIST accounts ...
@app.route("/accounts", methods=["GET"])
def list_accounts():
    """
    List all Accounts
    This endpoint will return all Accounts
    """
    app.logger.info("Request to list all Accounts")
    accounts = Account.all()
    results = [account.serialize() for account in accounts]
    app.logger.info("Returning %d accounts", len(results))
    return jsonify(results), status.HTTP_200_OK


######################################################################
# READ AN ACCOUNT
######################################################################

# ... place you code here to READ an account ...

@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_account(account_id):
    """
    Reads an Account
    This endpoint will read an Account based the account_id that is requested
    """
    app.logger.info("Request to read an Account with id: %s", account_id)
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")
    return jsonify(account.serialize()), status.HTTP_200_OK

######################################################################
# UPDATE AN EXISTING ACCOUNT
######################################################################

# ... place you code here to UPDATE an account ...
@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    """
    Update an Account
    This endpoint will update an Account based on the account_id that is requested
    """
    app.logger.info("Request to update an Account with id: %s", account_id)
    account = Account.find(account_id)
    
    if not account:
        app.logger.error("Account with id %s not found", account_id)
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")

    try:
        data = request.get_json()
        app.logger.info("Received data: %s", data)
        if not data:
            raise ValueError("No data provided")

        # Update only the fields provided in the request data
        for key, value in data.items():
            setattr(account, key, value)

        account.update()
        app.logger.info("Account after update: %s", account.serialize())
        return jsonify(account.serialize()), status.HTTP_200_OK

    except Exception as e:
        app.logger.error("Error updating account: %s", str(e))
        abort(status.HTTP_400_BAD_REQUEST, str(e))




######################################################################
# DELETE AN ACCOUNT
######################################################################

# ... place you code here to DELETE an account ...
@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    """
    Delete an Account
    This endpoint will delete an Account based on the account_id that is requested
    """
    app.logger.info("Request to delete an Account with id: %s", account_id)
    account = Account.find(account_id)
    
    if not account:
        app.logger.error("Account with id %s not found", account_id)
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")
    
    try:
        account.delete()
        app.logger.info("Account with id %s has been deleted", account_id)
        return "", status.HTTP_204_NO_CONTENT
    except Exception as e:
        app.logger.error("Error deleting account: %s", str(e))
        abort(status.HTTP_400_BAD_REQUEST, str(e))



######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )
