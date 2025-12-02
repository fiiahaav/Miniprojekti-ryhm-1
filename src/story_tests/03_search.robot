*** Settings ***
Resource    resource.robot
Suite Setup     Open Browser To Home
Suite Teardown  Close Browser

*** Variables ***
${SEARCH_URL}    ${HOME_URL}/get_references

*** Test Cases ***
Search By Title
    Go To    ${SEARCH_URL}
    Select From List By Value    id=type    articles
    Input Text    id=query    Test Article
    Click Button    xpath=//button[text()='Hae']
    Page Should Contain    Test Article

Search By Year
    Go To    ${SEARCH_URL}
    Input Text    id=year    2024
    Click Button    xpath=//button[text()='Hae']
    Page Should Contain    Test Article
    Page Should Contain    Test Book

Search By Type Returns No Results
    Go To    ${SEARCH_URL}
    Select From List By Value    id=type    inproceedings
    Input Text    id=query    Nonexistent
    Click Button    xpath=//button[text()='Hae']
    Page Should Contain    Ei löytynyt viitteitä.

Search By Query And Year
    Go To    ${SEARCH_URL}
    Select From List By Value    id=type    books
    Input Text    id=query    Test Book
    Input Text    id=year    2024
    Click Button    xpath=//button[text()='Hae']
    Page Should Contain    Test Book
