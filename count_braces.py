path = "force-app/main/default/classes/DonationTriggerHandlerTest.cls"

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

depth = 0
for i, line in enumerate(lines, start=1):
    opens = line.count("{")
    closes = line.count("}")
    depth += opens - closes
    if opens > 0 or closes > 0:
        print(f"Line {i:3d} | depth={depth:2d} | {line.rstrip()}")

print(f"\nFinal brace depth: {depth} (should be 0)")