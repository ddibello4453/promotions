Feature: The promotion store service back-end
    As a promotion Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my promotions

    Background:
        Given the following promotions
            | cust_promo_code  | type   | value | quantity  | start_date   | end_date     | active | product_id   | dev_created_at |
            | JULY4            | SAVING | 50    | 10        | 2024-03-05   | 2024-03-10   | True   | 33422        | 2024-03-05     |
            | JUN2             | BOGO   | 20    | 5         | 2024-03-05   | 2024-03-10   | True   | 2928383      | 2024-03-05     |

    Scenario: The server is running
        When I visit the "Home Page"
        Then I should see "promotion Demo RESTful Service" in the title
        And I should not see "404 Not Found"