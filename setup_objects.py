import os

files = {}

# ── PROGRAMME__C ─────────────────────────────────────────────

files["force-app/main/default/objects/Programme__c/Programme__c.object-meta.xml"] = '''<?xml version="1.0" encoding="UTF-8"?>
<CustomObject xmlns="http://soap.sforce.com/2006/04/metadata">
    <label>Programme</label>
    <pluralLabel>Programmes</pluralLabel>
    <nameField>
        <label>Programme Name</label>
        <type>Text</type>
    </nameField>
    <deploymentStatus>Deployed</deploymentStatus>
    <sharingModel>ReadWrite</sharingModel>
    <description>An NGO intervention programme operating in a specific South African province.</description>
</CustomObject>'''

files["force-app/main/default/objects/Programme__c/fields/Status__c.field-meta.xml"] = '''<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Status__c</fullName>
    <label>Status</label>
    <type>Picklist</type>
    <valueSet>
        <valueSetDefinition>
            <sorted>false</sorted>
            <value><fullName>Active</fullName><default>true</default><label>Active</label></value>
            <value><fullName>Inactive</fullName><default>false</default><label>Inactive</label></value>
            <value><fullName>Completed</fullName><default>false</default><label>Completed</label></value>
        </valueSetDefinition>
    </valueSet>
</CustomField>'''

files["force-app/main/default/objects/Programme__c/fields/Province__c.field-meta.xml"] = '''<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Province__c</fullName>
    <label>Province</label>
    <type>Picklist</type>
    <valueSet>
        <valueSetDefinition>
            <sorted>true</sorted>
            <value><fullName>Gauteng</fullName><default>false</default><label>Gauteng</label></value>
            <value><fullName>KwaZulu-Natal</fullName><default>false</default><label>KwaZulu-Natal</label></value>
            <value><fullName>Western Cape</fullName><default>false</default><label>Western Cape</label></value>
            <value><fullName>Eastern Cape</fullName><default>false</default><label>Eastern Cape</label></value>
            <value><fullName>Limpopo</fullName><default>false</default><label>Limpopo</label></value>
            <value><fullName>Mpumalanga</fullName><default>false</default><label>Mpumalanga</label></value>
            <value><fullName>North West</fullName><default>false</default><label>North West</label></value>
            <value><fullName>Free State</fullName><default>false</default><label>Free State</label></value>
            <value><fullName>Northern Cape</fullName><default>false</default><label>Northern Cape</label></value>
        </valueSetDefinition>
    </valueSet>
</CustomField>'''

files["force-app/main/default/objects/Programme__c/fields/Focus_Area__c.field-meta.xml"] = '''<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Focus_Area__c</fullName>
    <label>Focus Area</label>
    <type>Picklist</type>
    <valueSet>
        <valueSetDefinition>
            <sorted>false</sorted>
            <value><fullName>Youth Skills Development</fullName><default>false</default><label>Youth Skills Development</label></value>
            <value><fullName>Rural Food Security</fullName><default>false</default><label>Rural Food Security</label></value>
            <value><fullName>Early Childhood Education</fullName><default>false</default><label>Early Childhood Education</label></value>
            <value><fullName>Women Economic Empowerment</fullName><default>false</default><label>Women Economic Empowerment</label></value>
            <value><fullName>Healthcare Access</fullName><default>false</default><label>Healthcare Access</label></value>
            <value><fullName>Housing Support</fullName><default>false</default><label>Housing Support</label></value>
        </valueSetDefinition>
    </valueSet>
</CustomField>'''

files["force-app/main/default/objects/Programme__c/fields/Start_Date__c.field-meta.xml"] = '''<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Start_Date__c</fullName>
    <label>Start Date</label>
    <type>Date</type>
</CustomField>'''

files["force-app/main/default/objects/Programme__c/fields/Target_Beneficiaries__c.field-meta.xml"] = '''<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Target_Beneficiaries__c</fullName>
    <label>Target Beneficiaries</label>
    <type>Number</type>
    <precision>10</precision>
    <scale>0</scale>
</CustomField>'''

files["force-app/main/default/objects/Programme__c/fields/Total_Donations__c.field-meta.xml"] = '''<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Total_Donations__c</fullName>
    <label>Total Donations</label>
    <type>Currency</type>
    <precision>16</precision>
    <scale>2</scale>
    <defaultValue>0</defaultValue>
</CustomField>'''

files["force-app/main/default/objects/Programme__c/fields/Funding_Goal__c.field-meta.xml"] = '''<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Funding_Goal__c</fullName>
    <label>Funding Goal</label>
    <type>Currency</type>
    <precision>16</precision>
    <scale>2</scale>
</CustomField>'''

files["force-app/main/default/objects/Programme__c/fields/Funding_Progress__c.field-meta.xml"] = '''<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Funding_Progress__c</fullName>
    <label>Funding Progress (%)</label>
    <type>Percent</type>
    <formula>IF(Funding_Goal__c &gt; 0, (Total_Donations__c / Funding_Goal__c) * 100, 0)</formula>
    <formulaTreatBlanksAs>BlankAsZero</formulaTreatBlanksAs>
    <precision>5</precision>
    <scale>1</scale>
</CustomField>'''

# ── DONATION__C ───────────────────────────────────────────────

files["force-app/main/default/objects/Donation__c/Donation__c.object-meta.xml"] = '''<?xml version="1.0" encoding="UTF-8"?>
<CustomObject xmlns="http://soap.sforce.com/2006/04/metadata">
    <label>Donation</label>
    <pluralLabel>Donations</pluralLabel>
    <nameField>
        <label>Donation Number</label>
        <type>AutoNumber</type>
        <displayFormat>DON-{0000}</displayFormat>
    </nameField>
    <deploymentStatus>Deployed</deploymentStatus>
    <sharingModel>ControlledByParent</sharingModel>
    <description>A single financial contribution from a donor to a programme.</description>
</CustomObject>'''

files["force-app/main/default/objects/Donation__c/fields/Amount__c.field-meta.xml"] = '''<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Amount__c</fullName>
    <label>Amount (ZAR)</label>
    <type>Currency</type>
    <precision>16</precision>
    <scale>2</scale>
    <required>true</required>
</CustomField>'''

files["force-app/main/default/objects/Donation__c/fields/Donation_Date__c.field-meta.xml"] = '''<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Donation_Date__c</fullName>
    <label>Donation Date</label>
    <type>Date</type>
    <required>true</required>
    <defaultValue>TODAY()</defaultValue>
</CustomField>'''

files["force-app/main/default/objects/Donation__c/fields/Programme__c.field-meta.xml"] = '''<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Programme__c</fullName>
    <label>Programme</label>
    <type>MasterDetail</type>
    <referenceTo>Programme__c</referenceTo>
    <relationshipName>Donations</relationshipName>
    <relationshipLabel>Donations</relationshipLabel>
</CustomField>'''

files["force-app/main/default/objects/Donation__c/fields/Donor__c.field-meta.xml"] = '''<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Donor__c</fullName>
    <label>Donor</label>
    <type>Lookup</type>
    <referenceTo>Contact</referenceTo>
    <relationshipName>Donations</relationshipName>
    <relationshipLabel>Donations</relationshipLabel>
</CustomField>'''

files["force-app/main/default/objects/Donation__c/fields/Payment_Method__c.field-meta.xml"] = '''<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Payment_Method__c</fullName>
    <label>Payment Method</label>
    <type>Picklist</type>
    <valueSet>
        <valueSetDefinition>
            <sorted>false</sorted>
            <value><fullName>EFT</fullName><default>true</default><label>EFT</label></value>
            <value><fullName>Credit Card</fullName><default>false</default><label>Credit Card</label></value>
            <value><fullName>Cash</fullName><default>false</default><label>Cash</label></value>
            <value><fullName>Debit Order</fullName><default>false</default><label>Debit Order</label></value>
        </valueSetDefinition>
    </valueSet>
</CustomField>'''

files["force-app/main/default/objects/Donation__c/fields/Acknowledgement_Sent__c.field-meta.xml"] = '''<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Acknowledgement_Sent__c</fullName>
    <label>Acknowledgement Sent</label>
    <type>Checkbox</type>
    <defaultValue>false</defaultValue>
</CustomField>'''

# ── BENEFICIARY__C ────────────────────────────────────────────

files["force-app/main/default/objects/Beneficiary__c/Beneficiary__c.object-meta.xml"] = '''<?xml version="1.0" encoding="UTF-8"?>
<CustomObject xmlns="http://soap.sforce.com/2006/04/metadata">
    <label>Beneficiary</label>
    <pluralLabel>Beneficiaries</pluralLabel>
    <nameField>
        <label>Beneficiary Name</label>
        <type>Text</type>
    </nameField>
    <deploymentStatus>Deployed</deploymentStatus>
    <sharingModel>ReadWrite</sharingModel>
    <description>An individual receiving services from an NGO programme.</description>
</CustomObject>'''

files["force-app/main/default/objects/Beneficiary__c/fields/Programme__c.field-meta.xml"] = '''<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Programme__c</fullName>
    <label>Programme</label>
    <type>Lookup</type>
    <referenceTo>Programme__c</referenceTo>
    <relationshipName>Beneficiaries</relationshipName>
    <relationshipLabel>Beneficiaries</relationshipLabel>
</CustomField>'''

files["force-app/main/default/objects/Beneficiary__c/fields/Province__c.field-meta.xml"] = '''<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Province__c</fullName>
    <label>Province</label>
    <type>Picklist</type>
    <valueSet>
        <valueSetDefinition>
            <sorted>true</sorted>
            <value><fullName>Gauteng</fullName><default>false</default><label>Gauteng</label></value>
            <value><fullName>KwaZulu-Natal</fullName><default>false</default><label>KwaZulu-Natal</label></value>
            <value><fullName>Western Cape</fullName><default>false</default><label>Western Cape</label></value>
            <value><fullName>Eastern Cape</fullName><default>false</default><label>Eastern Cape</label></value>
            <value><fullName>Limpopo</fullName><default>false</default><label>Limpopo</label></value>
            <value><fullName>Mpumalanga</fullName><default>false</default><label>Mpumalanga</label></value>
            <value><fullName>North West</fullName><default>false</default><label>North West</label></value>
            <value><fullName>Free State</fullName><default>false</default><label>Free State</label></value>
            <value><fullName>Northern Cape</fullName><default>false</default><label>Northern Cape</label></value>
        </valueSetDefinition>
    </valueSet>
</CustomField>'''

files["force-app/main/default/objects/Beneficiary__c/fields/Age_Group__c.field-meta.xml"] = '''<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Age_Group__c</fullName>
    <label>Age Group</label>
    <type>Picklist</type>
    <valueSet>
        <valueSetDefinition>
            <sorted>false</sorted>
            <value><fullName>Child (0-12)</fullName><default>false</default><label>Child (0-12)</label></value>
            <value><fullName>Youth (13-24)</fullName><default>false</default><label>Youth (13-24)</label></value>
            <value><fullName>Adult (25-59)</fullName><default>false</default><label>Adult (25-59)</label></value>
            <value><fullName>Senior (60+)</fullName><default>false</default><label>Senior (60+)</label></value>
        </valueSetDefinition>
    </valueSet>
</CustomField>'''

files["force-app/main/default/objects/Beneficiary__c/fields/Urban_Rural__c.field-meta.xml"] = '''<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Urban_Rural__c</fullName>
    <label>Urban or Rural</label>
    <type>Picklist</type>
    <valueSet>
        <valueSetDefinition>
            <sorted>false</sorted>
            <value><fullName>Urban</fullName><default>false</default><label>Urban</label></value>
            <value><fullName>Rural</fullName><default>false</default><label>Rural</label></value>
        </valueSetDefinition>
    </valueSet>
</CustomField>'''

files["force-app/main/default/objects/Beneficiary__c/fields/Enrolment_Date__c.field-meta.xml"] = '''<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Enrolment_Date__c</fullName>
    <label>Enrolment Date</label>
    <type>Date</type>
    <defaultValue>TODAY()</defaultValue>
</CustomField>'''

# ── WRITE ALL FILES ───────────────────────────────────────────

written = 0
for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"  Written: {path}")
    written += 1

print(f"\nDone — {written} files written successfully.")