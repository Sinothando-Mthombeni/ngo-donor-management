import os

files = {}

# ── TRIGGER ───────────────────────────────────────────────────

files["force-app/main/default/triggers/DonationTrigger.trigger"] = '''trigger DonationTrigger on Donation__c (
    after insert,
    after update,
    after delete,
    after undelete
) {
    DonationTriggerHandler handler = new DonationTriggerHandler(
        Trigger.new,
        Trigger.old,
        Trigger.newMap,
        Trigger.oldMap
    );

    if (Trigger.isAfter) {
        if (Trigger.isInsert)   handler.afterInsert();
        if (Trigger.isUpdate)   handler.afterUpdate();
        if (Trigger.isDelete)   handler.afterDelete();
        if (Trigger.isUndelete) handler.afterUndelete();
    }
}'''

files["force-app/main/default/triggers/DonationTrigger.trigger-meta.xml"] = '''<?xml version="1.0" encoding="UTF-8"?>
<ApexTrigger xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>59.0</apiVersion>
    <status>Active</status>
</ApexTrigger>'''

# ── HANDLER CLASS ─────────────────────────────────────────────

files["force-app/main/default/classes/DonationTriggerHandler.cls"] = '''/**
 * DonationTriggerHandler
 *
 * Handles all business logic fired by DonationTrigger.
 *
 * Responsibilities:
 *  1. Recalculate Programme__c.Total_Donations__c on any
 *     donation insert, update, delete, or undelete.
 *  2. Flag high-value donors (>= R10,000) on their Contact record.
 *
 * Design: Thin trigger -> fat handler pattern.
 * All methods are bulkified - safe for 200-record batches.
 */
public with sharing class DonationTriggerHandler {

    private List<Donation__c> newDonations;
    private List<Donation__c> oldDonations;
    private Map<Id, Donation__c> newMap;
    private Map<Id, Donation__c> oldMap;

    @TestVisible
    private static final Decimal HIGH_VALUE_THRESHOLD = 10000;

    public DonationTriggerHandler(
        List<Donation__c> newList,
        List<Donation__c> oldList,
        Map<Id, Donation__c> newMap,
        Map<Id, Donation__c> oldMap
    ) {
        this.newDonations = newList;
        this.oldDonations = oldList;
        this.newMap       = newMap;
        this.oldMap       = oldMap;
    }

    // Entry Points

    public void afterInsert() {
        recalculateProgrammeTotals(newDonations, null);
        flagHighValueDonors(newDonations);
    }

    public void afterUpdate() {
        recalculateProgrammeTotals(newDonations, oldDonations);
    }

    public void afterDelete() {
        recalculateProgrammeTotals(null, oldDonations);
    }

    public void afterUndelete() {
        recalculateProgrammeTotals(newDonations, null);
    }

    // Core Logic

    /**
     * Recalculates Total_Donations__c on every affected Programme.
     * Pattern: collect IDs -> one aggregate query -> one DML call.
     * Never queries or performs DML inside a loop.
     */
    private void recalculateProgrammeTotals(
        List<Donation__c> newList,
        List<Donation__c> oldList
    ) {
        Set<Id> programmeIds = new Set<Id>();

        if (newList != null) {
            for (Donation__c d : newList) {
                if (d.Programme__c != null) {
                    programmeIds.add(d.Programme__c);
                }
            }
        }
        if (oldList != null) {
            for (Donation__c d : oldList) {
                if (d.Programme__c != null) {
                    programmeIds.add(d.Programme__c);
                }
            }
        }

        if (programmeIds.isEmpty()) return;

        // One aggregate SOQL - sums all donations per programme
        Map<Id, Decimal> totalsMap = new Map<Id, Decimal>();
        for (AggregateResult ar : [
            SELECT Programme__c progId, SUM(Amount__c) total
            FROM Donation__c
            WHERE Programme__c IN :programmeIds
            GROUP BY Programme__c
        ]) {
            totalsMap.put(
                (Id)      ar.get(\'progId\'),
                (Decimal) ar.get(\'total\')
            );
        }

        // Build update list - one DML statement
        List<Programme__c> toUpdate = new List<Programme__c>();
        for (Id progId : programmeIds) {
            Decimal total = totalsMap.containsKey(progId)
                ? totalsMap.get(progId)
                : 0;
            toUpdate.add(new Programme__c(
                Id = progId,
                Total_Donations__c = total
            ));
        }

        if (!toUpdate.isEmpty()) {
            update toUpdate;
        }
    }

    /**
     * Flags any Contact whose single donation meets or exceeds
     * the HIGH_VALUE_THRESHOLD by updating their Description.
     */
    private void flagHighValueDonors(List<Donation__c> donations) {
        Set<Id> highValueDonorIds = new Set<Id>();

        for (Donation__c d : donations) {
            if (d.Donor__c != null && d.Amount__c >= HIGH_VALUE_THRESHOLD) {
                highValueDonorIds.add(d.Donor__c);
            }
        }

        if (highValueDonorIds.isEmpty()) return;

        if (!Schema.sObjectType.Contact.isUpdateable()) {
            throw new AuraHandledException(
                \'Insufficient permissions to update Contact records.\'
            );
        }

        List<Contact> toUpdate = new List<Contact>();
        for (Id donorId : highValueDonorIds) {
            toUpdate.add(new Contact(
                Id = donorId,
                Description = \'High-Value Donor - donation threshold of R\'
                    + HIGH_VALUE_THRESHOLD.format()
                    + \' exceeded.\'
            ));
        }

        if (!toUpdate.isEmpty()) {
            update toUpdate;
        }
    }
}'''

files["force-app/main/default/classes/DonationTriggerHandler.cls-meta.xml"] = '''<?xml version="1.0" encoding="UTF-8"?>
<ApexClass xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>59.0</apiVersion>
    <status>Active</status>
</ApexClass>'''

# ── TEST CLASS ────────────────────────────────────────────────

files["force-app/main/default/classes/DonationTriggerHandlerTest.cls"] = '''/**
 * DonationTriggerHandlerTest
 *
 * Tests all business logic in DonationTriggerHandler.
 * Covers: insert, update, delete, bulk (200 records), high-value donor flagging.
 * Target coverage: 95%+
 */
@IsTest
public with sharing class DonationTriggerHandlerTest {

    @TestSetup
    static void setupData() {
        Programme__c prog = new Programme__c(
            Name                    = \'Rural Youth Skills - Limpopo\',
            Status__c               = \'Active\',
            Province__c             = \'Limpopo\',
            Focus_Area__c           = \'Youth Skills Development\',
            Target_Beneficiaries__c = 500,
            Funding_Goal__c         = 250000
        );
        insert prog;

        Contact donor = new Contact(
            FirstName = \'Sinothando\',
            LastName  = \'Test Donor\'
        );
        insert donor;
    }

    @IsTest
    static void testTotalDonationsOnInsert() {
        Programme__c prog  = [SELECT Id FROM Programme__c LIMIT 1];
        Contact      donor = [SELECT Id FROM Contact LIMIT 1];

        List<Donation__c> donations = new List<Donation__c>();
        for (Integer i = 0; i < 5; i++) {
            donations.add(new Donation__c(
                Programme__c     = prog.Id,
                Donor__c         = donor.Id,
                Amount__c        = 1000,
                Donation_Date__c = Date.today()
            ));
        }

        Test.startTest();
        insert donations;
        Test.stopTest();

        Programme__c result = [
            SELECT Total_Donations__c FROM Programme__c WHERE Id = :prog.Id
        ];
        System.assertEquals(
            5000,
            result.Total_Donations__c,
            \'Total should be R5000 after 5 x R1000 donations\'
        );
    }

    @IsTest
    static void testTotalRecalculatedOnUpdate() {
        Programme__c prog  = [SELECT Id FROM Programme__c LIMIT 1];
        Contact      donor = [SELECT Id FROM Contact LIMIT 1];

        Donation__c donation = new Donation__c(
            Programme__c     = prog.Id,
            Donor__c         = donor.Id,
            Amount__c        = 2000,
            Donation_Date__c = Date.today()
        );
        insert donation;

        Test.startTest();
        donation.Amount__c = 5000;
        update donation;
        Test.stopTest();

        Programme__c result = [
            SELECT Total_Donations__c FROM Programme__c WHERE Id = :prog.Id
        ];
        System.assertEquals(
            5000,
            result.Total_Donations__c,
            \'Total should update to R5000 after amount change\'
        );
    }

    @IsTest
    static void testTotalRecalculatedOnDelete() {
        Programme__c prog  = [SELECT Id FROM Programme__c LIMIT 1];
        Contact      donor = [SELECT Id FROM Contact LIMIT 1];

        Donation__c donation = new Donation__c(
            Programme__c     = prog.Id,
            Donor__c         = donor.Id,
            Amount__c        = 8000,
            Donation_Date__c = Date.today()
        );
        insert donation;

        Test.startTest();
        delete donation;
        Test.stopTest();

        Programme__c result = [
            SELECT Total_Donations__c FROM Programme__c WHERE Id = :prog.Id
        ];
        System.assertEquals(
            0,
            result.Total_Donations__c,
            \'Total should be R0 after deleting the only donation\'
        );
    }

    @IsTest
    static void testHighValueDonorFlagged() {
        Programme__c prog  = [SELECT Id FROM Programme__c LIMIT 1];
        Contact      donor = [SELECT Id FROM Contact LIMIT 1];

        Donation__c bigDonation = new Donation__c(
            Programme__c     = prog.Id,
            Donor__c         = donor.Id,
            Amount__c        = 15000,
            Donation_Date__c = Date.today()
        );

        Test.startTest();
        insert bigDonation;
        Test.stopTest();

        Contact result = [SELECT Description FROM Contact WHERE Id = :donor.Id];
        System.assert(
            result.Description != null &&
            result.Description.contains(\'High-Value Donor\'),
            \'Donor should be flagged after a R15000 donation\'
        );
    }

    @IsTest
    static void testBelowThresholdNotFlagged() {
        Programme__c prog  = [SELECT Id FROM Programme__c LIMIT 1];
        Contact      donor = [SELECT Id FROM Contact LIMIT 1];

        Donation__c smallDonation = new Donation__c(
            Programme__c     = prog.Id,
            Donor__c         = donor.Id,
            Amount__c        = 500,
            Donation_Date__c = Date.today()
        );

        Test.startTest();
        insert smallDonation;
        Test.stopTest();

        Contact result = [SELECT Description FROM Contact WHERE Id = :donor.Id];
        System.assert(
            result.Description == null ||
            !result.Description.contains(\'High-Value Donor\'),
            \'Donor should NOT be flagged for a R500 donation\'
        );
    }

    @IsTest
    static void testBulk200Donations() {
        Programme__c prog  = [SELECT Id FROM Programme__c LIMIT 1];
        Contact      donor = [SELECT Id FROM Contact LIMIT 1];

        List<Donation__c> bulk = new List<Donation__c>();
        for (Integer i = 0; i < 200; i++) {
            bulk.add(new Donation__c(
                Programme__c     = prog.Id,
                Donor__c         = donor.Id,
                Amount__c        = 100,
                Donation_Date__c = Date.today()
            ));
        }

        Test.startTest();
        insert bulk;
        Test.stopTest();

        Programme__c result = [
            SELECT Total_Donations__c FROM Programme__c WHERE Id = :prog.Id
        ];
        System.assertEquals(
            20000,
            result.Total_Donations__c,
            \'Total should be R20000 for 200 x R100 donations\'
        );
    }

    @IsTest
    static void testFundingProgressFormula() {
        Programme__c prog  = [SELECT Id FROM Programme__c LIMIT 1];
        Contact      donor = [SELECT Id FROM Contact LIMIT 1];

        List<Donation__c> donations = new List<Donation__c>();
        for (Integer i = 0; i < 5; i++) {
            donations.add(new Donation__c(
                Programme__c     = prog.Id,
                Donor__c         = donor.Id,
                Amount__c        = 25000,
                Donation_Date__c = Date.today()
            ));
        }

        Test.startTest();
        insert donations;
        Test.stopTest();

        Programme__c result = [
            SELECT Total_Donations__c, Funding_Progress__c, Funding_Goal__c
            FROM Programme__c WHERE Id = :prog.Id
        ];
        System.assertEquals(125000, result.Total_Donations__c,
            \'Total donations should be R125000\');
        System.assertEquals(50, result.Funding_Progress__c,
            \'Funding progress should be 50% of R250000 goal\');
    }
}'''

files["force-app/main/default/classes/DonationTriggerHandlerTest.cls-meta.xml"] = '''<?xml version="1.0" encoding="UTF-8"?>
<ApexClass xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>59.0</apiVersion>
    <status>Active</status>
</ApexClass>'''

# ── WRITE ALL FILES ───────────────────────────────────────────

written = 0
for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"  Written: {path}")
    written += 1

print(f"\nDone — {written} files written successfully.")