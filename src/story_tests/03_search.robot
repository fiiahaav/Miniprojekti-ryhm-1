*** Settings ***
Resource    resource.robot
Suite Setup     Open Browser To Home
Suite Teardown  Close Browser

*** Variables ***
${SEARCH_URL}    ${HOME_URL}/get_references

*** Test Cases ***
User Can Search By Title
    Go To    ${SEARCH_URL}
    Wait Until Element Is Visible    id=type    timeout=5s
    Select From List By Value       id=type    articles
    Wait Until Element Is Visible    id=query    timeout=5s
    Input Text    id=query    Test Article
    Wait Until Element Is Visible    xpath=//button[text()='Hae']    timeout=5s
    Click Button    xpath=//button[text()='Hae']
    Wait Until Page Contains    Test Article    timeout=5s

User Can Search By Year
    Go To    ${SEARCH_URL}
    Wait Until Element Is Visible    id=year    timeout=5s
    Input Text    id=year    2024
    Wait Until Element Is Visible    xpath=//button[text()='Hae']    timeout=5s
    Click Button    xpath=//button[text()='Hae']
    Wait Until Page Contains    Test Article    timeout=5s
    Wait Until Page Contains    Test Book    timeout=5s

User Can Search By Type Returns No Results
    Go To    ${SEARCH_URL}
    Wait Until Element Is Visible    id=type    timeout=5s
    Select From List By Value    id=type    inproceedings
    Wait Until Element Is Visible    id=query    timeout=5s
    Input Text    id=query    Nonexistent
    Wait Until Element Is Visible    xpath=//button[text()='Hae']    timeout=5s
    Click Button    xpath=//button[text()='Hae']
    Wait Until Page Contains    Ei löytynyt viitteitä.    timeout=5s

User Can Search By Query And Year
    Go To    ${SEARCH_URL}
    Wait Until Element Is Visible    id=type    timeout=5s
    Select From List By Value    id=type    books
    Wait Until Element Is Visible    id=query    timeout=5s
    Input Text    id=query    Test Book
    Wait Until Element Is Visible    id=year    timeout=5s
    Input Text    id=year    2024
    Wait Until Element Is Visible    xpath=//button[text()='Hae']    timeout=5s
    Click Button    xpath=//button[text()='Hae']
    Wait Until Page Contains    Test Book    timeout=5s
