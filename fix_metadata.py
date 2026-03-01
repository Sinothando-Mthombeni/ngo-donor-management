import os

files = {
    "force-app/main/default/classes/DonationTriggerHandlerTest.cls-meta.xml": """<?xml version="1.0" encoding="UTF-8"?>
<ApexClass xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>62.0</apiVersion>
    <status>Active</status>
</ApexClass>""",

    "force-app/main/default/classes/DonationTriggerHandler.cls-meta.xml": """<?xml version="1.0" encoding="UTF-8"?>
<ApexClass xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>62.0</apiVersion>
    <status>Active</status>
</ApexClass>""",

    "force-app/main/default/triggers/DonationTrigger.trigger-meta.xml": """<?xml version="1.0" encoding="UTF-8"?>
<ApexTrigger xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>62.0</apiVersion>
    <status>Active</status>
</ApexTrigger>""",
}

for path, content in files.items():
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content.strip())
    print(f"Updated: {path}")