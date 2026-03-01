/**
 * ProgrammeDashboardController
 *
 * Apex controller for the programmeDashboard LWC.
 * Returns all programmes with donation totals, funding progress,
 * and a map of beneficiary counts keyed by Programme Id.
 */
public with sharing class ProgrammeDashboardController {

    @AuraEnabled(cacheable=true)
    public static Map<String, Object> getDashboardData() {

        if (!Schema.sObjectType.Programme__c.isAccessible()) {
            throw new AuraHandledException(
                'Insufficient permissions to access Programme data.'
            );
        }

        // Query all programmes with calculated fields
        List<Programme__c> programmes = [
            SELECT Id,
                   Name,
                   Status__c,
                   Province__c,
                   Focus_Area__c,
                   Total_Donations__c,
                   Funding_Goal__c,
                   Funding_Progress__c,
                   Target_Beneficiaries__c,
                   Start_Date__c
            FROM Programme__c
            ORDER BY Province__c ASC, Name ASC
        ];

        // Query all beneficiaries for province breakdown
        List<Beneficiary__c> beneficiaries = [
            SELECT Id, Province__c, Programme__c, Urban_Rural__c
            FROM Beneficiary__c
        ];

        // Build beneficiary count map keyed by Programme Id
        Map<Id, Integer> beneficiaryCounts = new Map<Id, Integer>();
        for (Programme__c prog : programmes) {
            beneficiaryCounts.put(prog.Id, 0);
        }
        for (Beneficiary__c b : beneficiaries) {
            if (b.Programme__c != null && beneficiaryCounts.containsKey(b.Programme__c)) {
                beneficiaryCounts.put(
                    b.Programme__c,
                    beneficiaryCounts.get(b.Programme__c) + 1
                );
            }
        }

        // Return everything in one map — single callout from LWC
        Map<String, Object> result = new Map<String, Object>();
        result.put('programmes', programmes);
        result.put('beneficiaries', beneficiaries);
        result.put('beneficiaryCounts', beneficiaryCounts);

        return result;
    }
}