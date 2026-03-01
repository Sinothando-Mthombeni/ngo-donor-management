# NGO Donor & Programme Management System

A portfolio-grade Salesforce CRM application built to manage donors,
programmes, and beneficiaries for a South African nonprofit organisation.

This project is the operational counterpart to the
[NIDS Socioeconomic Wellbeing Analysis](https://github.com/Sinothando-Mthombeni/nids-socioeconomic-analysis)
— where that project identified persistent inequality across South African
provinces using household survey data, this system provides the platform
an NGO would use to act on those findings: tracking donor funding,
managing intervention programmes by province, and monitoring beneficiary
reach across urban and rural communities.

---

## Features

- Custom data model with three objects — Programme, Donation, Beneficiary
- Apex trigger recalculating total donations per programme on every
  insert, update, delete, and undelete event
- Automatic high-value donor flagging for donations above R10,000
- Formula field tracking funding progress as a percentage of goal
- Province and urban/rural classification across all nine SA provinces
- Lightning Web Component dashboard showing live programme statistics
- Full Apex test suite with 7 test cases and 86%+ code coverage
- Bulk-safe trigger logic validated against 200-record test batches

---

## Data Model
```
Account (standard)
    |
    └── Contact (standard) ── Donor__c ──> Donation__c <── Programme__c (Master)
                                                               |
                                                           Beneficiary__c
```

### Objects

| Object | Type | Description |
|---|---|---|
| Programme__c | Custom | NGO intervention by province and focus area |
| Donation__c | Custom | Financial contribution linked to programme and donor |
| Beneficiary__c | Custom | Individual receiving programme services |

### Key Fields

| Field | Object | Type | Description |
|---|---|---|---|
| Total_Donations__c | Programme__c | Currency | Auto-calculated by trigger |
| Funding_Goal__c | Programme__c | Currency | Target funding amount |
| Funding_Progress__c | Programme__c | Formula (%) | Total / Goal * 100 |
| Province__c | Programme__c, Beneficiary__c | Picklist | All 9 SA provinces |
| Urban_Rural__c | Beneficiary__c | Picklist | Urban or Rural |
| Amount__c | Donation__c | Currency | Donation value in ZAR |
| Donor__c | Donation__c | Lookup | Linked Contact record |

---

## Apex Architecture
```
DonationTrigger.trigger          <- Thin trigger, delegates to handler
    |
    └── DonationTriggerHandler.cls   <- All business logic
            |
            ├── recalculateProgrammeTotals()
            |       Collect IDs -> one aggregate SOQL -> one DML
            |       Bulkified: safe for 200-record batches
            |
            └── flagHighValueDonors()
                    Flags Contact.Description for donations >= R10,000

DonationTriggerHandlerTest.cls   <- 7 test cases, 86%+ coverage
    ├── testTotalDonationsOnInsert
    ├── testTotalRecalculatedOnUpdate
    ├── testTotalRecalculatedOnDelete
    ├── testHighValueDonorFlagged
    ├── testBelowThresholdNotFlagged
    ├── testBulk200Donations
    └── testFundingProgressFormula
```

---

## Project Structure
```
ngo-donor-management/
|
├── force-app/main/default/
│   ├── objects/
│   │   ├── Programme__c/         <- Object + 8 fields
│   │   ├── Donation__c/          <- Object + 6 fields
│   │   └── Beneficiary__c/       <- Object + 5 fields
│   |
│   ├── triggers/
│   │   └── DonationTrigger.trigger
│   |
│   ├── classes/
│   │   ├── DonationTriggerHandler.cls
│   │   └── DonationTriggerHandlerTest.cls
│   |
│   └── lwc/
│       └── programmeDashboard/   <- Live stats component
|
├── setup_objects.py              <- Data model setup script
├── setup_apex.py                 <- Apex setup script
└── README.md
```

---

## How to Deploy
```bash
# 1. Clone the repository
git clone https://github.com/Sinothando-Mthombeni/ngo-donor-management.git
cd ngo-donor-management

# 2. Authenticate with your Salesforce org
sf org login web --alias MyOrg

# 3. Deploy data model
sf project deploy start --source-dir force-app/main/default/objects --target-org MyOrg

# 4. Deploy Apex classes and trigger
sf project deploy start --source-dir force-app/main/default/classes --target-org MyOrg
sf project deploy start --source-dir force-app/main/default/triggers --target-org MyOrg

# 5. Run tests
sf apex run test --class-names DonationTriggerHandlerTest --target-org MyOrg --result-format human --synchronous

# 6. Deploy LWC component
sf project deploy start --source-dir force-app/main/default/lwc --target-org MyOrg
```

---

## Test Results
```
DonationTriggerHandlerTest.testBelowThresholdNotFlagged   Pass
DonationTriggerHandlerTest.testBulk200Donations           Pass
DonationTriggerHandlerTest.testHighValueDonorFlagged      Pass
DonationTriggerHandlerTest.testTotalDonationsOnInsert     Pass
DonationTriggerHandlerTest.testTotalRecalculatedOnDelete  Pass
DonationTriggerHandlerTest.testTotalRecalculatedOnUpdate  Pass
DonationTriggerHandlerTest.testFundingProgressFormula     Pass

Pass Rate: 100% | Tests Ran: 7
```

---

## Connection to NIDS Research

The NIDS Socioeconomic Wellbeing Analysis revealed that household
per-capita expenditure is lowest in Limpopo, Eastern Cape, and
KwaZulu-Natal, with persistent urban-rural gaps across all survey
waves. This system operationalises that insight — programmes are
classified by the exact same provincial and urban-rural dimensions,
allowing an NGO to direct funding toward the communities the data
identified as most vulnerable.

---

## Tech Stack

| Layer | Tools |
|---|---|
| Platform | Salesforce Developer Edition |
| Backend | Apex, SOQL |
| Frontend | Lightning Web Components |
| Data Model | Custom Objects, Formula Fields |
| Tooling | Salesforce CLI, VS Code, Git |
| Testing | Apex Test Classes, sf apex run test |

---

## About

Built as part of a Salesforce development portfolio by
Sinothando Mthombeni — BSc Information Technology, North-West University.

Contact: sinopapi7@gmail.com
GitHub: https://github.com/Sinothando-Mthombeni
LinkedIn: https://linkedin.com/in/sinothando-mthombeni-211166363/