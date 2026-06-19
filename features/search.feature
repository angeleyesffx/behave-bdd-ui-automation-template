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
  Scenario: Search for a non-existent product returns no results
    When I search for no_results
    Then I should see no products found

  @smoke @TC-S003
  Scenario: Empty search returns the full product catalogue
    When I submit an empty search
    Then I should see the results
