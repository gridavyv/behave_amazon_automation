Feature: Search_results

      Background: get to 'ebay.com'
        Given Navigate to 'ebay.com'

      Scenario: Search results are relevant on the specific pages
        And [Header] Enter query 'oculus'
        Then [Header] Click on button 'Search'
        Then Verify all items from page '2' to '5' related to query 'oculus'