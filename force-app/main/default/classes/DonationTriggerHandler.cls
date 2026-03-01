/**
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
                (Id)      ar.get('progId'),
                (Decimal) ar.get('total')
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
                'Insufficient permissions to update Contact records.'
            );
        }

        List<Contact> toUpdate = new List<Contact>();
        for (Id donorId : highValueDonorIds) {
            toUpdate.add(new Contact(
                Id = donorId,
                Description = 'High-Value Donor - donation threshold of R'
                    + HIGH_VALUE_THRESHOLD.format()
                    + ' exceeded.'
            ));
        }

        if (!toUpdate.isEmpty()) {
            update toUpdate;
        }
    }
}