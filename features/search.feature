@ui @feature-search
Feature: Search
  As a shop visitor,
  I want to search for products by keyword,
  So I can quickly find items that interest me.

  Background:
    Given I navigate to the Products page

  @smoke @TC-S001
  Scenario Outline: Successful search returns relevant results
    When I search for <data>
    Then I should see the results

    Examples:
      | data  |
      | dress |
      | top   |

  @negative @TC-S002
  Scenario: Search filters the product catalogue
    When I search for dress
    Then the search results page is shown
