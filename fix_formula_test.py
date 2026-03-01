path = "force-app/main/default/classes/DonationTriggerHandlerTest.cls"

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

fixed_lines = []
for line in lines:
    if "Funding_Progress__c" in line and "assertEquals" in line:
        line = "        System.assertEquals(50.0, result.Funding_Progress__c, 'Progress should be 50 percent');\n"
    fixed_lines.append(line)

with open(path, "w", encoding="utf-8", newline="\n") as f:
    f.writelines(fixed_lines)

print("Fixed funding progress assertion")

# Show the fixed line
for i, line in enumerate(fixed_lines, start=1):
    if "Funding_Progress__c" in line and "assertEquals" in line:
        print(f"Line {i}: {line.rstrip()}")