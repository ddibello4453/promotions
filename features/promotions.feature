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
        Then I should see "Promotion Demo RESTful Service" in the title
        And I should not see "404 Not Found"

    Scenario: Create a Promotion
    When I visit the "Home Page"
    And I set the "Cust Promo Code" to "SUMMERSALE"
    And I select "Percent" in the "Type" dropdown
    And I set the "Value" to "25"
    And I set the "Quantity" to "100"
    And I set the "Start Date" to "05-15-2024"
    And I set the "End Date" to "05-17-2024"
    And I select "True" in the "Active" dropdown
    And I set the "Product ID" to "9588"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Promo ID" field
    And I press the "Clear" button
    Then the "Promo ID" field should be empty
    And the "Cust Promo Code" field should be empty
    And the "Type" field should be empty
    And the "Value" field should be empty
    And the "Quantity" field should be empty
    And the "Start Date" field should be empty
    And the "End Date" field should be empty
    And the "Active" field should be empty
    And the "Product ID" field should be empty
    When I paste the "Promo ID" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "SUMMERSALE" in the "Cust Promo Code" field
    And I should see "Percent" in the "Type" dropdown
    And I should see "25" in the "Value" field
    And I should see "100" in the "Quantity" field
    And I should see "2024-05-15" in the "Start Date" field
    And I should see "2024-05-17" in the "End Date" field
    And I should see "True" in the "Active" dropdown
    And I should see "9588" in the "Product ID" field