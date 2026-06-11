@api @feature-auth
Feature: API Authentication
  As a user of the platform,
  I want to authenticate via API,
  So I can receive a token to access protected resources.

  Background:
    Given I get the endpoint from TokenAPI

  @smoke @TC-A001
  Scenario: Successful authentication returns home page data
    When the request sends POST to the TokenAPI
    And I get the endpoint from HomeAPI
    And the request sends GET to the HomeAPI
    Then I should see the response

  @negative @TC-A002
  Scenario: Authentication with invalid credentials returns 401
    When the request sends POST to the TokenAPI with invalid credentials
    Then the response status is 401
