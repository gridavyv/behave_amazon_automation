Feature: Banner_carousel

    Background: get to 'ebay.com'
        Given Navigate to 'ebay.com'

    Scenario: Example
        And Print banners as webelements

    Scenario: Verify there are 4 banners in carousel
        And [BannerCarousel] Verify there are '4' banners in the carousel

    Scenario: Verify images are changing every 4 seconds
        And [BannerCarousel] Verify that every '3.5' seconds new banner is displayed. The number of banners: '4'.
#
    Scenario: User can pause the carousel
        And [BannerCarousel] Click on 'Pause' button
        And [BannerCarousel] Remember the current banner
        And [BannerCarousel] Verify that banner is not changing for '10' seconds

    Scenario: User can resume the carousel
        And [BannerCarousel] Click on 'Pause' button
        Then [BannerCarousel] Click on 'Play' button
        And [BannerCarousel] Verify that every '3.5' seconds new banner is displayed. The number of banners: '4'.

    Scenario: Verify all 4 banner links work
        And Verify '4' banner links work

    Scenario: Verify 'Go to next' and 'Go to previous' buttons change the banner
        And [BannerCarousel] Remember the current banner
        And [BannerCarousel] Click on 'Go to next' button
        And [BannerCarousel] Verify the banner is changed
        And [BannerCarousel] Click on 'Go to previous' button
        And [BannerCarousel] Verify the banner is the same as in the beginning of the secenario execution.
