"""
Test cases for Pet Model
"""

import os
import logging
from unittest import TestCase
from wsgi import app
from service.models import Promotions, Type, DataValidationError, db
from .factories import PromotionsFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  Promotions   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestPromotions(TestCase):
    """Test Cases for Promotions Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Promotions).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_promotions(self):
        """It should create a Promotions"""
        promotions = PromotionsFactory()
        promotions.create()
        self.assertIsNotNone(promotions.promo_id)
        found = Promotions.all()
        self.assertEqual(len(found), 1)
        data = Promotions.find(promotions.promo_id)
        self.assertEqual(data.cust_promo_code, promotions.cust_promo_code)
        self.assertEqual(data.type, promotions.type)
        self.assertEqual(data.value, promotions.value)
        self.assertEqual(data.quantity, promotions.quantity)
        self.assertEqual(data.start_date, promotions.start_date)
        self.assertEqual(data.end_date, promotions.end_date)
        self.assertEqual(data.active, promotions.active)
        self.assertEqual(data.product_id, promotions.product_id)
        self.assertEqual(data.dev_created_at, promotions.dev_created_at)

    def test_delete_a_promotion(self):
        """It should Delete a Pet"""
        promotions = PromotionsFactory()
        promotions.create()
        self.assertEqual(len(Promotions.all()), 1)
        # delete the promotion and make sure it isn't in the database
        promotions.delete()
        self.assertEqual(len(Promotions.all()), 0)

    # Todo: Add your test cases here...
