"""
TestPromotions API Service Test Suite
"""

import os
import logging
from unittest import TestCase
from wsgi import app
from service.common import status
from service.models import db, Promotions
from .factories import PromotionsFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/promotions"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestYourResourceService(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Promotions).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_promotions(self):
        """It should Create a new Promotions"""
        test_promotions = PromotionsFactory()
        logging.debug("Test Promotions: %s", test_promotions.serialize())
        response = self.client.post(BASE_URL, json=test_promotions.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_promotions = response.get_json()
        self.assertEqual(
            new_promotions["cust_promo_code"], test_promotions.cust_promo_code
        )
        self.assertEqual(new_promotions["type"], test_promotions.type.name)
        self.assertEqual(new_promotions["value"], test_promotions.value)
        self.assertEqual(new_promotions["quantity"], test_promotions.quantity)
        self.assertEqual(
            new_promotions["start_date"], test_promotions.start_date.isoformat()
        )
        self.assertEqual(
            new_promotions["end_date"], test_promotions.end_date.isoformat()
        )
        self.assertEqual(new_promotions["active"], test_promotions.active)
        self.assertEqual(new_promotions["product_id"], test_promotions.product_id)
        self.assertEqual(
            new_promotions["dev_created_at"], test_promotions.dev_created_at.isoformat()
        )

        def test_get_promotion_list(self):
            """It should Get a list of Promotions"""
            self._create_promotions(5)
            response = self.client.get(BASE_URL)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.get_json()
            self.assertEqual(len(data), 5)

        # Todo: uncomment this code when get_promotions is implemented
        # Check that the location header was correct
        # response = self.client.get(location)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # new_promotions = response.get_json()
        # self.assertEqual(
        #     new_promotions["cust_promo_code"], test_promotions.cust_promo_code
        # )
        # self.assertEqual(new_promotions["type"], test_promotions.type.name)
        # self.assertEqual(new_promotions["value"], test_promotions.value)
        # self.assertEqual(new_promotions["quantity"], test_promotions.quantity)
        # self.assertEqual(
        #     new_promotions["start_date"], test_promotions.start_date.isoformat()
        # )
        # self.assertEqual(
        #     new_promotions["end_date"], test_promotions.end_date.isoformat()
        # )
        # self.assertEqual(new_promotions["active"], test_promotions.active)
        # self.assertEqual(new_promotions["product_id"], test_promotions.product_id)
        # self.assertEqual(
        #     new_promotions["dev_created_at"], test_promotions.dev_created_at.isoformat()
        # )
