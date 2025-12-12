*** Settings ***
Resource    resource.robot
Library     OperatingSystem
Library     SeleniumLibrary

Test Setup       Setup Browser And Seed Data
Suite Teardown   Close Browser

*** Variables ***
# Reuse the browser download directory from resource.robot
${SINGLE_DIR}    ${DOWNLOAD_DIR}
${ALL_DIR}       ${DOWNLOAD_DIR}

*** Keywords ***
Setup Browser And Seed Data
    # Ensure directories exist and are empty
    Create Directory    ${SINGLE_DIR}
    Create Directory    ${ALL_DIR}
    Delete All Files In Directory    ${SINGLE_DIR}
    Delete All Files In Directory    ${ALL_DIR}

    # Open browser with default download dir
    Open Browser To Home

    # Seed DB with one article for download tests
    Seed Test Data

Setup Browser Empty
    # Ensure directories exist and are empty, but do NOT seed DB
    Create Directory    ${SINGLE_DIR}
    Create Directory    ${ALL_DIR}
    Delete All Files In Directory    ${SINGLE_DIR}
    Delete All Files In Directory    ${ALL_DIR}

    Open Browser To Home

Seed Test Data
    Go To    ${HOME_URL}
    Select From List By Value    id=lahde    article
    Click Button    id=submit-btn
    Input Text    name=author    Download Tester
    Input Text    name=title     Download Test Article
    Input Text    name=journal   Journal DL
    Input Text    name=year      2024
    Input Text    name=month     1
    Click Button   xpath=//button[contains(text(),'Lisää')]
    Wait Until Page Contains    Download Test Article

Wait For File
    [Arguments]    ${dir}
    Wait Until Keyword Succeeds    10x    1s    Directory Should Contain Files    ${dir}

Directory Should Contain Files
    [Arguments]    ${dir}
    ${files}=    List Files In Directory    ${dir}
    Should Not Be Empty    ${files}

Delete All Files In Directory
    [Arguments]    ${dir}
    Create Directory    ${dir}
    ${files}=    List Files In Directory    ${dir}
    FOR    ${f}    IN    @{files}
        Remove File    ${dir}${/}${f}
    END

Clear Any Popup
    Run Keyword And Ignore Error    Handle Alert    ACCEPT

Switch Download Directory
    [Arguments]    ${dir}
    # No-op: download directory is fixed via Chrome options in Open Browser To Home
    Log    Using fixed download directory: ${DOWNLOAD_DIR}

*** Test Cases ***
Download Single BibTeX Works
    Clear Any Popup
    Go To    ${HOME_URL}
    Delete All Files In Directory    ${SINGLE_DIR}
    Switch Download Directory    ${SINGLE_DIR}
    Click Element    xpath=(//a[contains(@class,'download-link')])[1]
    Wait For File    ${SINGLE_DIR}

Download All BibTeX Works
    Clear Any Popup
    Go To    ${HOME_URL}
    Delete All Files In Directory    ${ALL_DIR}
    Switch Download Directory    ${ALL_DIR}
    Click Button    xpath=//button[text()='Lataa Kaikki BibTeX']
    Wait For File    ${ALL_DIR}
