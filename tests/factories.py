"""
Test Factory to make fake objects for testing
"""

from datetime import date

import factory
from factory.fuzzy import FuzzyChoice, FuzzyInteger, FuzzyDate
from service.models import Promotions, Type


class PromotionsFactory(factory.Factory):
    """Creates fake pets that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Promotions

    promo_id = factory.Sequence(lambda n: n)
    cust_promo_code = factory.Faker("word")
    type = FuzzyChoice(choices=[Type.PERCENT, Type.SAVING, Type.BOGO])
    value = FuzzyInteger(0, 100)
    quantity = FuzzyInteger(0, 1000)
    start_date = FuzzyDate(date.today())
    end_date = FuzzyDate(date.today())
    active = FuzzyChoice(choices=[True, False])
    product_id = factory.Faker("random_number")
    dev_created_at = date.today()
