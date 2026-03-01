trigger DonationTrigger on Donation__c (
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
}