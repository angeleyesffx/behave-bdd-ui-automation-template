@ui @feature-login
Feature: Login MyHome
  As a user of MyHome,
  I want to sign in with my credentials,
  So I can access the platform.

  Background:
    Given I navigate to the Login page

  @smoke @TC-L001
  Scenario: Successful login with valid credentials redirects to home page
    When I fill the credentials from valid user
    Then I should see the my home page

  @negative @TC-L002
  Scenario: Login with invalid credentials shows authentication error
    When I fill the credentials from invalid user
    Then I should see an authentication error message
