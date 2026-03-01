with open('force-app/main/default/classes/DonationTriggerHandlerTest.cls', 'rb') as f:
    content = f.read()

lines = content.split(b'\n')
print('Total lines:', len(lines))
print()

for i, line in enumerate(lines[130:160], start=131):
    decoded = line.decode('utf-8', errors='replace')
    print(f'{i}: {decoded}')