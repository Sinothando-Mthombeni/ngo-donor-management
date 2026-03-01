@IsTest
public with sharing class DonationTriggerHandlerTest {

    @TestSetup
    static void setupData() {
        Programme__c prog = new Programme__c(
            Name                    = 'Rural Youth Skills - Limpopo',
            Status__c               = 'Active',
            Province__c             = 'Limpopo',
            Focus_Area__c           = 'Youth Skills Development',
            Target_Beneficiaries__c = 500,
            Funding_Goal__c         = 250000
        );
        insert prog;
        Contact donor = new Contact(
            FirstName = 'Sinothando',
            LastName  = 'Test Donor'
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
        Programme__c result = [SELECT Total_Donations__c FROM Programme__c WHERE Id = :prog.Id];
        System.assertEquals(5000, result.Total_Donations__c, 'Total should be R5000');
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
        Programme__c result = [SELECT Total_Donations__c FROM Programme__c WHERE Id = :prog.Id];
        System.assertEquals(5000, result.Total_Donations__c, 'Total should be R5000 after update');
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
        Programme__c result = [SELECT Total_Donations__c FROM Programme__c WHERE Id = :prog.Id];
        System.assertEquals(0, result.Total_Donations__c, 'Total should be R0 after delete');
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
        System.assert(result.Description != null && result.Description.contains('High-Value Donor'), 'Should be flagged');
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
        System.assert(result.Description == null || !result.Description.contains('High-Value Donor'), 'Should not be flagged');
    }

    @IsTest
    static void testBulk200Donations() {
        Programme__c prog  = [SELECT Id FROM Programme__c LIMIT 1];
        Contact      donor = [SELECT Id FROM Contact LIMIT 1];
        List<Donation__c> bulkDonations = new List<Donation__c>();
        for (Integer i = 0; i < 200; i++) {
            bulkDonations.add(new Donation__c(
                Programme__c     = prog.Id,
                Donor__c         = donor.Id,
                Amount__c        = 100,
                Donation_Date__c = Date.today()
            ));
        }
        Test.startTest();
        insert bulkDonations;
        Test.stopTest();
        Programme__c result = [SELECT Total_Donations__c FROM Programme__c WHERE Id = :prog.Id];
        System.assertEquals(20000, result.Total_Donations__c, 'Total should be R20000');
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
        Programme__c result = [SELECT Total_Donations__c, Funding_Progress__c FROM Programme__c WHERE Id = :prog.Id];
        System.assertEquals(125000, result.Total_Donations__c, 'Total should be R125000');
        System.assertEquals(5000.0, result.Funding_Progress__c, 'Progress should be 5000.0 internally');
    }
}