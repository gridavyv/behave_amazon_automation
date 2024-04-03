Feature: test action chains

    Background: get to 'ebay.com'
        Given Navigate to 'ebay.com'

    Scenario: Mouse hover 'Toys' category
      And Mouse hover 'Toys' category