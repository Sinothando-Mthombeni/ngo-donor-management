List<Programme__c> progs = [SELECT Id, Name FROM Programme__c LIMIT 1];
System.debug('Programme__c accessible: ' + progs);

Map<String, Schema.SObjectField> fields = Schema.SObjectType.Programme__c.fields.getMap();
for (String fieldName : fields.keySet()) {
    System.debug('Field: ' + fieldName);
}