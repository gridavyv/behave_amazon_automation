Feature: Search

    Background: get to 'ebay.com'
        Given Navigate to 'ebay.com'

    Scenario: Verify search category by default
        And [Header] Verify search category 'All Categories'

    Scenario: Search results are relevant to valid query
        And [Header] Enter query 'oculus'
        Then [Header] Click on button 'Search'
        Then Verify page title contains query 'oculus for sale'
        And [Header] Verify search category 'PC & Console VR Headsets'
        And Verify all results are related to query 'oculus'

    Scenario: Invalid query
        And [Header] Enter query 'asd@jf%%jal123sdjfk@@@sdalf'
        Then [Header] Click on button 'Search'
        Then Verify page title contains query 'asd@jf%%jal123sdjfk@@@sdalf for sale'
        And [Header] Verify search category 'All Categories'
        And [Result answer] Verify result feedback 'No exact matches found'

    Scenario: Empty query
        And [Header] Click on button 'Search'
        Then Verify page title contains query 'Shop by Category'

    Scenario: Verify number of items per page by default
        And [Header] Enter query 'oculus'
        Then [Header] Click on button 'Search'
        Then Verify num of items per page '60'

    Scenario: Number of presented results (excluding carousel) equals to items per page
        Then [Header] Enter query 'oculus'
        Then [Header] Click on button 'Search'
        Then Verify num of presented results (excluding carousel results:8) equals to num items per page

    Scenario: Find on the page number 1 the item with lowest price and print its title
        And [Header] Enter query 'oculus'
        Then [Header] Click on button 'Search'
        Then Find on the page number 1 the item with the lowest price and print its title

