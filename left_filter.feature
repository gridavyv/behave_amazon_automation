Feature: Left filter

    Background: get to 'ebay.com'
        Given Navigate to 'ebay.com'

    Scenario: Titles of filtered results are relevant to valid query
        And [Header] Enter query 'iphone'
        Then [Header] Click on button 'Search'
        And [LeftFilter] Filter 'Model': select option 'Apple iPhone 12'
        And [LeftFilter] Filter 'Storage Capacity': select option '256 GB'
        And [Results] Collect links to results sub pages
        Then [Results] Verify result titles are related to 'iPhone 12'

    Scenario: Specs of filtered results are relevant to valid query
        And [Header] Enter query 'iphone'
        Then [Header] Click on button 'Search'
        And [LeftFilter] Select an option from a filter
        | Filter           | Option          |
        | Network          | Verizon         |
        | Model            | Apple iPhone 12 |
        | Storage Capacity | 256 GB          |
        And [ResultsSubPage] Verify in spec the label 'Storage Capacity' matches the value '256 GB'