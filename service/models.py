"""
Models for Promotions

All of the models are stored in this module

Models
------
Promotions - Promotions used in the e-commerce

Attributes:
-----------

promo_id (integer) - the unique promo_id of the promotion
cust_promo_code	(string) - the user-facing code user can use to implement the promotion
type (string) - the type of the promotion (percent, saving, bogo)
value (integer) - the value of the promotion (only applies for percent and saving)
quantity (integer) - the number of times the promotion can be used
start_date (date) - the date the promotion starts
end_date (date) - the date the promotion ends
active (boolean) - True for promotions that are active to be used
product_id (string) - the unique promo_id of the product the promotion is associated with
dev_created_at (date) - the date the promotion is created in the system
"""

import logging
from enum import Enum
from datetime import date
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class Type(Enum):
    """Enumeration of valid Type"""

    PERCENT = 1
    SAVING = 2
    BOGO = 3


class Promotions(db.Model):
    """
    Class that represents a Promotions
    """

    ##################################################
    # Table Schema
    ##################################################
    promo_id = db.Column(db.Integer, primary_key=True)
    cust_promo_code = db.Column(db.String(63), nullable=False)
    type = db.Column(db.Enum(Type), nullable=False)
    value = db.Column(db.Integer, nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date(), nullable=True)
    end_date = db.Column(db.Date(), nullable=True)
    active = db.Column(db.Boolean(), nullable=False)
    product_id = db.Column(db.Integer, nullable=True)
    dev_created_at = db.Column(db.Date(), nullable=False, default=date.today())

    def __repr__(self):
        return f"<Promotions {self.cust_promo_code} promo_id=[{self.promo_id}]>"

    def create(self):
        """
        Creates a Promotions to the database
        """
        logger.info("Creating %s", self.cust_promo_code)
        self.promo_id = None  # pylint: disable=invalid-cust_promo_code
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error creating record: %s", self)
            raise DataValidationError(e) from e

    def update(self):
        """
        Updates a Promotions to the database
        """
        logger.info("Saving %s", self.cust_promo_code)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error updating record: %s", self)
            raise DataValidationError(e) from e

    def delete(self):
        """Removes a Promotions from the data store"""
        logger.info("Deleting %s", self.cust_promo_code)
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error deleting record: %s", self)
            raise DataValidationError(e) from e

    def serialize(self):
        """Serializes a Promotions into a dictionary"""
        return {
            "promo_id": self.promo_id,
            "cust_promo_code": self.cust_promo_code,
            "type": self.type.name,
            "value": self.value,
            "quantity": self.quantity,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "active": self.active,
            "product_id": self.product_id,
            "dev_created_at": self.dev_created_at.isoformat(),
        }

    def deserialize(self, data):
        """
        Deserializes a Promotions from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.cust_promo_code = data["cust_promo_code"]
            self.type = getattr(Type, data["type"])
            self.value = data["value"]
            self.quantity = data["quantity"]
            self.start_date = date.fromisoformat(data["start_date"])
            self.end_date = date.fromisoformat(data["end_date"])
            self.active = data["active"]
            self.product_id = data["product_id"]
            self.dev_created_at = date.fromisoformat(data["dev_created_at"])
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid Promotions: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Promotions: body of request contained bad or no data "
                + str(error)
            ) from error
        return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def all(cls):
        """Returns all of the Promotions in the database"""
        logger.info("Processing all Promotions")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a Promotions by it's ID"""
        logger.info("Processing lookup for promo_id %s ...", by_id)
        return cls.query.session.get(cls, by_id)

    @classmethod
    def find_by_cust_promo_id(cls, cust_promo_code):
        """Returns all Promotions with the given cust_promo_code

        Args:
            cust_promo_code (string): the cust_promo_code of the Promotions you want to match
        """
        logger.info("Processing cust_promo_code query for %s ...", cust_promo_code)
        return cls.query.filter(cls.cust_promo_code == cust_promo_code)
