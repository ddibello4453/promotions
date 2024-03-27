"""
TestPromotions API Service Test Suite
"""

import os
import logging
from datetime import date, timedelta
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

    def _create_promotions(self, count):
        """Factory method to create promotion in bulk"""
        promotions = []
        for _ in range(count):
            test_promotion = PromotionsFactory()
            response = self.client.post(BASE_URL, json=test_promotion.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test promotion",
            )
            new_promotion = response.get_json()
            test_promotion.promo_id = new_promotion["promo_id"]
            promotions.append(test_promotion)
        return promotions

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

        # Check that the location header was correct
        response = self.client.get(location)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
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

    #####
    # Test List Promotion
    def test_update_promotion(self):
        """It should Update an existing Promotion"""
        # create a promotion to update
        test_promotions = PromotionsFactory()
        response = self.client.post(BASE_URL, json=test_promotions.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the promotion
        new_promotion = response.get_json()
        logging.debug(new_promotion)
        new_promotion["category"] = "unknown"
        response = self.client.put(
            f"{BASE_URL}/{new_promotion['promo_id']}", json=new_promotion
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_promotion = response.get_json()
        self.assertEqual(updated_promotion["type"], test_promotions.type.name)

    def test_get_promotion_list(self):
        """It should Get a list of Promotions"""
        self._create_promotions(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    def test_get_promotion(self):
        """It should Get a single Promotion"""
        # get the id of a promotion
        test_promotion = self._create_promotions(1)[0]
        print("error log test_promotion")
        print(test_promotion)
        response = self.client.get(f"{BASE_URL}/{test_promotion.promo_id}")
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["promo_id"], test_promotion.promo_id)

    def test_get_promotion_not_found(self):
        """It should not Get a Promotion thats not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])

    def test_delete_promotion(self):
        """It should Delete a Promotion"""
        test_promotion = self._create_promotions(1)[0]
        response = self.client.delete(f"{BASE_URL}/{test_promotion.promo_id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)
        # make sure they are deleted
        response = self.client.get(f"{BASE_URL}/{test_promotion.promo_id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cancel(self):
        """It should cancel a promotion by changing its end date to yesterday."""
        # create a promotion to update
        test_promotions = PromotionsFactory()
        response = self.client.post(BASE_URL, json=test_promotions.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # cancel the promotion
        new_promotion = response.get_json()
        logging.debug(new_promotion)
        new_promotion["end_date"] = (date.today() - timedelta(days=1)).isoformat()
        new_promotion["active"] = False
        response = self.client.put(
            f"{BASE_URL}/{new_promotion['promo_id']}", json=new_promotion
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


######################################################################
#  T E S T   S A D   P A T H S
######################################################################
class TestSadPaths(TestCase):
    """Test REST Exception Handling"""

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()

    def test_method_not_allowed(self):
        """It should not allow update without a promotions id"""
        response = self.client.put(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_promotion_no_data(self):
        """It should not Create a Promotion with missing data"""
        response = self.client.post(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_promotion_no_content_type(self):
        """It should not Create a Promotion with no content type"""
        response = self.client.post(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_promotion_wrong_content_type(self):
        """It should not Create a Promotion with the wrong content type"""
        response = self.client.post(BASE_URL, data="hello", content_type="text/html")
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_promotion_bad_active(self):
        """It should not Create a Promotion with bad available data"""
        test_promotion = PromotionsFactory()
        logging.debug(test_promotion)
        # change available to a string
        test_promotion.active = "true"
        response = self.client.post(BASE_URL, json=test_promotion.serialize())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_pet_bad_type(self):
        """It should not Create a Promotion with bad type data"""
        promotions = PromotionsFactory()
        logging.debug(promotions)
        # change gender to a bad string
        test_promotion = promotions.serialize()
        test_promotion["type"] = "percent"  # wrong case
        response = self.client.post(BASE_URL, json=test_promotion)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
