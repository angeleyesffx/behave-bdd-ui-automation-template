@ui @feature-search
Feature: Search
  As a web surfer,
  I want to find information online,
  So I can learn new things and get tasks done.

  Background:
    Given I navigate to the Google Home page

  @smoke @TC-S001
  Scenario Outline: Successful search returns relevant results
    When I search for <data>
    Then I should see the results

    Examples:
      | data   |
      | python |
      | ruby   |

  @negative @TC-S002
  Scenario: Search action navigates away from the home page
    When I search for python
    Then the URL should contain the search query
