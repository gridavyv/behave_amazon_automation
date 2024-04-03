Feature: Category links in container under header

    Background: get to 'ebay.com'
        Given Navigate to 'ebay.com'

    @regression
    Scenario Outline: Verify category links SubPage title
        And [MainPage CategoryLinksContainer] Click on '<link_text>'
        Then [SubPage] Verify page title '<exp_page_title>'

    Examples:
    | link_text             | exp_page_title                                              |
#    | Saved                 | Sign in or Register                                         |
    | Motors                | eBay Motors: Auto Parts and Vehicles                        |
#    | Electronics           | Electronics products for sale                               |
#    | Collectibles          | Collectibles & Art products for sale                        |
#    | Home & Garden         | Home & Garden products for sale                             |
#    | Fashion               | Clothing, Shoes & Accessories for sale                      |
#    | Toys                  | Toys & Hobbies products for sale                            |
#    | Sporting Goods        | Sporting Goods for sale                                     |
#    | Business & Industrial | Business & Industrial products for sale                     |
#    | Jewelry & Watches     | Jewelry & Watches for sale                                  |
#    | eBay Live             | eBay Live                                                   |
#    | Refurbished           | eBay Refurbished Products for Sale: Phones, Laptops & More  |

    @regression
    Scenario Outline: Verify category links SubPage PageContainerTop title
        And [MainPage CategoryLinksContainer] Click on '<link_text>'
        Then [SubPage PageContainerTop] Verify title '<exp_cont_title>'

    Examples:
    | link_text             | exp_cont_title                |
    | Motors                | eBay Motors                   |
#    | Electronics           | Electronics                   |
#    | Collectibles          | Collectibles & Art            |
#    | Home & Garden         | Home & Garden                 |
#    | Fashion               | Clothing, Shoes & Accessories |
#    | Toys                  | Toys & Hobbies                |
#    | Sporting Goods        | Sporting Goods & Equipment    |
#    | Business & Industrial | Business & Industrial         |
    | Jewelry & Watches     | Jewelry & Watches             |
    | Refurbished           | eBay Refurbished              |

    @regression @smoke
    Scenario: Verify category link by default
        And [MainPage CategoryLinksContainer] Verify 'Home' is default category






