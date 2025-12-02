*** Settings ***
Resource    resource.robot
Suite Setup    Open Browser To Home
Suite Teardown    Close Browser

*** Test Cases ***
User Can Delete Article
    Go To    ${HOME_URL}
    Select From List By Value    id=lahde    article
    Click Button    id=submit-btn

    Input Text    name=author    Del Author
    Input Text    name=title     Article To Delete
    Input Text    name=journal   Del Journal
    Input Text    name=year      2025
    Click Button  xpath=//button[text()='Lisää']

    Go To    ${HOME_URL}
    Click Button    xpath=//div[contains(@class,'source-entry')]//strong[text()='Article To Delete']/../form/button[contains(@class,'delete-btn')]
    Sleep    1s
    Handle Alert    accept
    Sleep    1s
    Page Should Not Contain    Article To Delete


