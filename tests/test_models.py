"""
Test cases for Promotions Model
"""

import os
import logging
from unittest import TestCase
from unittest.mock import patch
from datetime import date, timedelta
from wsgi import app
from service.models import Promotions, Type, DataValidationError, db
from .factories import PromotionsFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  PROMOTIONS   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestCaseBase(TestCase):
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
        promotions = Promotions(
            cust_promo_code="CHRISTMAS PROMO",
            type=Type.PERCENT,
            value=25,
            quantity=100,
            active=True,
            dev_created_at=date.today(),
        )
        self.assertEqual(
            str(promotions), "<Promotions CHRISTMAS PROMO promo_id=[None]>"
        )
        self.assertTrue(promotions is not None)
        self.assertEqual(promotions.promo_id, None)
        self.assertEqual(promotions.cust_promo_code, "CHRISTMAS PROMO")
        self.assertEqual(promotions.type, Type.PERCENT)
        self.assertEqual(promotions.value, 25)
        self.assertEqual(promotions.quantity, 100)
        self.assertEqual(promotions.active, True)
        self.assertEqual(promotions.value, 25)
        self.assertEqual(promotions.dev_created_at, date.today())
        promotions = Promotions(
            cust_promo_code="CHRISTMAS PROMO",
            type=Type.BOGO,
            active=False,
            dev_created_at=date.today(),
        )
        self.assertEqual(promotions.type, Type.BOGO)
        self.assertEqual(promotions.active, False)

    def test_add_a_promotion(self):
        """It should Create a promotion and add it to the database"""
        promotions = Promotions.all()
        self.assertEqual(promotions, [])
        promotions = Promotions(
            cust_promo_code="PROMO",
            type=Type.PERCENT,
            value=10,
            quantity=10,
            active=True,
            dev_created_at=date.today(),
        )
        self.assertTrue(promotions is not None)
        self.assertEqual(promotions.promo_id, None)
        promotions.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(promotions.promo_id)
        promotions = Promotions.all()
        self.assertEqual(len(promotions), 1)

    def test_read_a_promotion(self):
        """It should Read a Promotion"""
        promotions = PromotionsFactory()
        logging.debug(promotions)
        promotions.promo_id = None
        promotions.create()
        self.assertIsNotNone(promotions.promo_id)
        # Fetch it back
        found_promotions = Promotions.find(promotions.promo_id)
        self.assertEqual(found_promotions.promo_id, promotions.promo_id)
        self.assertEqual(found_promotions.cust_promo_code, promotions.cust_promo_code)
        self.assertEqual(found_promotions.type, promotions.type)
        self.assertEqual(found_promotions.value, promotions.value)
        self.assertEqual(found_promotions.quantity, promotions.quantity)
        self.assertEqual(found_promotions.start_date, promotions.start_date)
        self.assertEqual(found_promotions.end_date, promotions.end_date)
        self.assertEqual(found_promotions.active, promotions.active)
        self.assertEqual(found_promotions.product_id, promotions.product_id)
        self.assertEqual(found_promotions.dev_created_at, promotions.dev_created_at)

    def test_update_a_promotion(self):
        """It should Update a Promotion"""
        promotions = PromotionsFactory()
        logging.debug(promotions)
        promotions.promo_id = None
        promotions.create()
        logging.debug(promotions)
        self.assertIsNotNone(promotions.promo_id)
        # Change it an save it
        promotions.value = 15
        original_id = promotions.promo_id
        promotions.update()
        self.assertEqual(promotions.promo_id, original_id)
        self.assertEqual(promotions.value, 15)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        promotions = Promotions.all()
        self.assertEqual(len(promotions), 1)
        self.assertEqual(promotions[0].promo_id, original_id)
        self.assertEqual(promotions[0].value, 15)

    def test_update_no_id(self):
        """It should not Update a Promotion with no id"""
        promotions = PromotionsFactory()
        logging.debug(promotions)
        promotions.promo_id = None
        self.assertRaises(DataValidationError, promotions.update)

    def test_delete_a_promotion(self):
        """It should Delete a Promotion"""
        promotions = PromotionsFactory()
        promotions.create()
        self.assertEqual(len(Promotions.all()), 1)
        # delete the promotion and make sure it isn't in the database
        promotions.delete()
        self.assertEqual(len(Promotions.all()), 0)

    def test_list_all_promotions(self):
        """It should List all Promotions in the database"""
        promotions = Promotions.all()
        self.assertEqual(promotions, [])
        # Create 5 Promotions
        for _ in range(5):
            promotions = PromotionsFactory()
            promotions.create()
        # See if we get back 5 promotions
        promotions = Promotions.all()
        self.assertEqual(len(promotions), 5)

    def test_serialize_a_promotions(self):
        """It should serialize a Promotions"""
        promotions = PromotionsFactory()
        data = promotions.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("promo_id", data)
        self.assertEqual(data["promo_id"], promotions.promo_id)
        self.assertIn("cust_promo_code", data)
        self.assertEqual(data["cust_promo_code"], promotions.cust_promo_code)
        self.assertIn("type", data)
        self.assertEqual(data["type"], promotions.type.name)
        self.assertIn("value", data)
        self.assertEqual(data["value"], promotions.value)
        self.assertIn("quantity", data)
        self.assertEqual(data["quantity"], promotions.quantity)
        self.assertIn("start_date", data)
        self.assertEqual(date.fromisoformat(data["start_date"]), promotions.start_date)
        self.assertIn("end_date", data)
        self.assertEqual(date.fromisoformat(data["end_date"]), promotions.end_date)
        self.assertIn("active", data)
        self.assertEqual(data["active"], promotions.active)
        self.assertIn("product_id", data)
        self.assertEqual(data["product_id"], promotions.product_id)
        self.assertIn("dev_created_at", data)
        self.assertEqual(
            date.fromisoformat(data["dev_created_at"]), promotions.dev_created_at
        )

    def test_deserialize_a_promotions(self):
        """It should de-serialize a Promotions"""
        data = PromotionsFactory().serialize()
        promotions = Promotions()
        promotions.deserialize(data)
        self.assertNotEqual(promotions, None)
        self.assertEqual(promotions.promo_id, None)
        self.assertEqual(promotions.cust_promo_code, data["cust_promo_code"])
        self.assertEqual(promotions.type.name, data["type"])
        self.assertEqual(promotions.value, data["value"])
        self.assertEqual(promotions.quantity, data["quantity"])
        self.assertEqual(promotions.start_date, date.fromisoformat(data["start_date"]))
        self.assertEqual(promotions.end_date, date.fromisoformat(data["end_date"]))
        self.assertEqual(promotions.active, data["active"])
        self.assertEqual(promotions.product_id, data["product_id"])
        self.assertEqual(
            promotions.dev_created_at, date.fromisoformat(data["dev_created_at"])
        )

    def test_deserialize_missing_data(self):
        """It should not deserialize a Promotions with missing data"""
        data = {"promo_id": 1, "cust_promo_code": "PROMO5", "type": "BOGO"}
        promotions = Promotions()
        self.assertRaises(DataValidationError, promotions.deserialize, data)

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        data = "this is not a dictionary"
        promotions = Promotions()
        self.assertRaises(DataValidationError, promotions.deserialize, data)

    def test_deserialize_bad_available(self):
        """It should not deserialize a bad available attribute"""
        test_promotions = PromotionsFactory()
        data = test_promotions.serialize()
        data["active"] = "true"
        promotions = Promotions()
        self.assertRaises(DataValidationError, promotions.deserialize, data)

    def test_deserialize_bad_type(self):
        """It should not deserialize a bad gender attribute"""
        test_promotions = PromotionsFactory()
        data = test_promotions.serialize()
        data["type"] = "percent"  # wrong case
        promotions = Promotions()
        self.assertRaises(DataValidationError, promotions.deserialize, data)

    def test_cancel(self):
        """It should test whether a promotion has been cancelled successfully"""
        promotions = PromotionsFactory()
        logging.debug(promotions)
        promotions.promo_id = None
        promotions.create()
        logging.debug(promotions)
        self.assertIsNotNone(promotions.promo_id)
        # Change it an save it
        promotions.end_date = date.today() - timedelta(days=1)
        promotions.active = False
        original_id = promotions.promo_id
        promotions.update()
        self.assertEqual(promotions.promo_id, original_id)
        self.assertEqual(promotions.end_date, date.today() - timedelta(days=1))
        self.assertEqual(promotions.active, False)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        promotions = Promotions.all()
        self.assertEqual(len(promotions), 1)
        self.assertEqual(promotions[0].promo_id, original_id)
        self.assertEqual(
            promotions[0].end_date,
            date.today() - timedelta(days=1),
        )
        self.assertEqual(promotions[0].active, False)


######################################################################
#  T E S T   E X C E P T I O N   H A N D L E R S
######################################################################
class TestExceptionHandlers(TestCaseBase):
    """Promotions Model Exception Handlers"""

    @patch("service.models.db.session.commit")
    def test_create_exception(self, exception_mock):
        """It should catch a create exception"""
        exception_mock.side_effect = Exception()
        promotions = PromotionsFactory()
        self.assertRaises(DataValidationError, promotions.create)

    @patch("service.models.db.session.commit")
    def test_update_exception(self, exception_mock):
        """It should catch a update exception"""
        exception_mock.side_effect = Exception()
        promotions = PromotionsFactory()
        self.assertRaises(DataValidationError, promotions.update)

    @patch("service.models.db.session.commit")
    def test_delete_exception(self, exception_mock):
        """It should catch a delete exception"""
        exception_mock.side_effect = Exception()
        promotions = PromotionsFactory()
        self.assertRaises(DataValidationError, promotions.delete)
