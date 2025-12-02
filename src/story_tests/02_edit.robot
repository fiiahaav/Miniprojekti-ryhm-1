*** Settings ***
Resource    resource.robot
Suite Setup     Open Browser To Home
Suite Teardown  Close Browser

*** Test Cases ***
User Can Edit Article Successfully
    # Step 1: Open home and create a new article to edit
    Go To    ${HOME_URL}
    Select From List By Value    id=lahde    article
    Click Button    id=submit-btn
    Wait Until Location Contains    /add_article    timeout=5s

    Input Text    name=author    Original Author
    Input Text    name=title     Original Title
    Input Text    name=journal   Original Journal
    Input Text    name=year      2022
    Click Button  xpath=//button[text()='Lisää']

    # Verify it is added
    Go To    ${HOME_URL}
    Wait Until Page Contains    Original Title    timeout=5s

    # Step 2: Click Edit for the article
    Click Link    xpath=//div[contains(@class,'source-entry')]//strong[text()='Original Title']/../a[contains(text(),'Muokkaa')]
    Wait Until Page Contains Element    xpath=//button[text()='Tallenna muutokset']    timeout=5s

    # Step 3: Change values
    Input Text    name=title     Updated Title
    Click Button  xpath=//button[text()='Tallenna muutokset']

    # Step 4: Back to home page and verify
    Go To    ${HOME_URL}
    Wait Until Page Contains    Updated Title    timeout=5s
    Page Should Not Contain    Original Title
