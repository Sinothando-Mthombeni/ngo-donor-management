path = "force-app/main/default/classes/DonationTriggerHandlerTest.cls"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Rename the variable 'bulk' to 'bulkDonations' throughout the file
fixed = content.replace("List<Donation__c> bulk ", "List<Donation__c> bulkDonations ")
fixed = fixed.replace("bulk.add(", "bulkDonations.add(")
fixed = fixed.replace("insert bulk;", "insert bulkDonations;")

with open(path, "w", encoding="utf-8", newline="\n") as f:
    f.write(fixed)

print("Fixed: renamed 'bulk' to 'bulkDonations'")

# Verify
with open(path, "r", encoding="utf-8") as f:
    verify = f.read()

print(f"'bulk' standalone still present: {' bulk ' in verify}")
print(f"'bulkDonations' present: {'bulkDonations' in verify}")