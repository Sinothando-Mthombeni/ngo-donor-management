Programme__c p1 = new Programme__c();
p1.Name = 'Rural Youth Skills - Limpopo';
p1.put('Status__c', 'Active');
p1.put('Province__c', 'Limpopo');
p1.put('Focus_Area__c', 'Youth Skills Development');
p1.put('Target_Beneficiaries__c', 500);
p1.put('Funding_Goal__c', 250000);
p1.put('Start_Date__c', Date.today());
insert p1;

Programme__c p2 = new Programme__c();
p2.Name = 'Early Childhood Education - Eastern Cape';
p2.put('Status__c', 'Active');
p2.put('Province__c', 'Eastern Cape');
p2.put('Focus_Area__c', 'Early Childhood Education');
p2.put('Target_Beneficiaries__c', 300);
p2.put('Funding_Goal__c', 180000);
p2.put('Start_Date__c', Date.today());
insert p2;

Programme__c p3 = new Programme__c();
p3.Name = 'Women Economic Empowerment - KZN';
p3.put('Status__c', 'Active');
p3.put('Province__c', 'KwaZulu-Natal');
p3.put('Focus_Area__c', 'Women Economic Empowerment');
p3.put('Target_Beneficiaries__c', 200);
p3.put('Funding_Goal__c', 150000);
p3.put('Start_Date__c', Date.today());
insert p3;

Programme__c p4 = new Programme__c();
p4.Name = 'Rural Food Security - North West';
p4.put('Status__c', 'Active');
p4.put('Province__c', 'North West');
p4.put('Focus_Area__c', 'Rural Food Security');
p4.put('Target_Beneficiaries__c', 400);
p4.put('Funding_Goal__c', 200000);
p4.put('Start_Date__c', Date.today());
insert p4;

Programme__c p5 = new Programme__c();
p5.Name = 'Healthcare Access - Mpumalanga';
p5.put('Status__c', 'Active');
p5.put('Province__c', 'Mpumalanga');
p5.put('Focus_Area__c', 'Healthcare Access');
p5.put('Target_Beneficiaries__c', 350);
p5.put('Funding_Goal__c', 175000);
p5.put('Start_Date__c', Date.today());
insert p5;

System.debug('Programmes inserted: 5');

Contact c1 = new Contact(FirstName='Thabo', LastName='Nkosi');
Contact c2 = new Contact(FirstName='Lerato', LastName='Dlamini');
Contact c3 = new Contact(FirstName='Zanele', LastName='Mokoena');
Contact c4 = new Contact(FirstName='Sipho', LastName='Mahlangu');
Contact c5 = new Contact(FirstName='Nomsa', LastName='Zulu');
insert new List<Contact>{c1, c2, c3, c4, c5};
System.debug('Contacts inserted: 5');

Donation__c d1 = new Donation__c();
d1.put('Programme__c', p1.Id);
d1.put('Donor__c', c1.Id);
d1.put('Amount__c', 75000);
d1.put('Donation_Date__c', Date.today());
d1.put('Payment_Method__c', 'EFT');
insert d1;

Donation__c d2 = new Donation__c();
d2.put('Programme__c', p1.Id);
d2.put('Donor__c', c2.Id);
d2.put('Amount__c', 50000);
d2.put('Donation_Date__c', Date.today());
d2.put('Payment_Method__c', 'EFT');
insert d2;

Donation__c d3 = new Donation__c();
d3.put('Programme__c', p2.Id);
d3.put('Donor__c', c3.Id);
d3.put('Amount__c', 90000);
d3.put('Donation_Date__c', Date.today());
d3.put('Payment_Method__c', 'Credit Card');
insert d3;

Donation__c d4 = new Donation__c();
d4.put('Programme__c', p2.Id);
d4.put('Donor__c', c4.Id);
d4.put('Amount__c', 45000);
d4.put('Donation_Date__c', Date.today());
d4.put('Payment_Method__c', 'Debit Order');
insert d4;

Donation__c d5 = new Donation__c();
d5.put('Programme__c', p3.Id);
d5.put('Donor__c', c5.Id);
d5.put('Amount__c', 80000);
d5.put('Donation_Date__c', Date.today());
d5.put('Payment_Method__c', 'EFT');
insert d5;

Donation__c d6 = new Donation__c();
d6.put('Programme__c', p3.Id);
d6.put('Donor__c', c1.Id);
d6.put('Amount__c', 15000);
d6.put('Donation_Date__c', Date.today());
d6.put('Payment_Method__c', 'EFT');
insert d6;

Donation__c d7 = new Donation__c();
d7.put('Programme__c', p4.Id);
d7.put('Donor__c', c2.Id);
d7.put('Amount__c', 60000);
d7.put('Donation_Date__c', Date.today());
d7.put('Payment_Method__c', 'EFT');
insert d7;

Donation__c d8 = new Donation__c();
d8.put('Programme__c', p5.Id);
d8.put('Donor__c', c3.Id);
d8.put('Amount__c', 55000);
d8.put('Donation_Date__c', Date.today());
d8.put('Payment_Method__c', 'Credit Card');
insert d8;

System.debug('Donations inserted: 8');

Beneficiary__c b1 = new Beneficiary__c();
b1.Name = 'Buhle Sithole';
b1.put('Programme__c', p1.Id);
b1.put('Province__c', 'Limpopo');
b1.put('Age_Group__c', 'Youth (13-24)');
b1.put('Urban_Rural__c', 'Rural');
b1.put('Enrolment_Date__c', Date.today());
insert b1;

Beneficiary__c b2 = new Beneficiary__c();
b2.Name = 'Mpho Langa';
b2.put('Programme__c', p1.Id);
b2.put('Province__c', 'Limpopo');
b2.put('Age_Group__c', 'Youth (13-24)');
b2.put('Urban_Rural__c', 'Rural');
b2.put('Enrolment_Date__c', Date.today());
insert b2;

Beneficiary__c b3 = new Beneficiary__c();
b3.Name = 'Thandeka Mthembu';
b3.put('Programme__c', p1.Id);
b3.put('Province__c', 'Limpopo');
b3.put('Age_Group__c', 'Adult (25-59)');
b3.put('Urban_Rural__c', 'Rural');
b3.put('Enrolment_Date__c', Date.today());
insert b3;

Beneficiary__c b4 = new Beneficiary__c();
b4.Name = 'Lindiwe Dube';
b4.put('Programme__c', p2.Id);
b4.put('Province__c', 'Eastern Cape');
b4.put('Age_Group__c', 'Child (0-12)');
b4.put('Urban_Rural__c', 'Rural');
b4.put('Enrolment_Date__c', Date.today());
insert b4;

Beneficiary__c b5 = new Beneficiary__c();
b5.Name = 'Ayanda Ntuli';
b5.put('Programme__c', p2.Id);
b5.put('Province__c', 'Eastern Cape');
b5.put('Age_Group__c', 'Child (0-12)');
b5.put('Urban_Rural__c', 'Rural');
b5.put('Enrolment_Date__c', Date.today());
insert b5;

Beneficiary__c b6 = new Beneficiary__c();
b6.Name = 'Nompumelelo Khumalo';
b6.put('Programme__c', p3.Id);
b6.put('Province__c', 'KwaZulu-Natal');
b6.put('Age_Group__c', 'Adult (25-59)');
b6.put('Urban_Rural__c', 'Urban');
b6.put('Enrolment_Date__c', Date.today());
insert b6;

Beneficiary__c b7 = new Beneficiary__c();
b7.Name = 'Fatima Cassim';
b7.put('Programme__c', p3.Id);
b7.put('Province__c', 'KwaZulu-Natal');
b7.put('Age_Group__c', 'Adult (25-59)');
b7.put('Urban_Rural__c', 'Urban');
b7.put('Enrolment_Date__c', Date.today());
insert b7;

Beneficiary__c b8 = new Beneficiary__c();
b8.Name = 'Refilwe Tau';
b8.put('Programme__c', p4.Id);
b8.put('Province__c', 'North West');
b8.put('Age_Group__c', 'Senior (60+)');
b8.put('Urban_Rural__c', 'Rural');
b8.put('Enrolment_Date__c', Date.today());
insert b8;

Beneficiary__c b9 = new Beneficiary__c();
b9.Name = 'Johannes Pretorius';
b9.put('Programme__c', p4.Id);
b9.put('Province__c', 'North West');
b9.put('Age_Group__c', 'Adult (25-59)');
b9.put('Urban_Rural__c', 'Rural');
b9.put('Enrolment_Date__c', Date.today());
insert b9;

Beneficiary__c b10 = new Beneficiary__c();
b10.Name = 'Precious Shabangu';
b10.put('Programme__c', p5.Id);
b10.put('Province__c', 'Mpumalanga');
b10.put('Age_Group__c', 'Adult (25-59)');
b10.put('Urban_Rural__c', 'Rural');
b10.put('Enrolment_Date__c', Date.today());
insert b10;

System.debug('Beneficiaries inserted: 10');
System.debug('=== Seed complete: 5 programmes, 5 donors, 8 donations, 10 beneficiaries ===');