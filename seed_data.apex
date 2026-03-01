// Create Programmes
List<Programme__c> programmes = new List<Programme__c>{
    new Programme__c(
        Name = 'Rural Youth Skills - Limpopo',
        Status__c = 'Active',
        Province__c = 'Limpopo',
        Focus_Area__c = 'Youth Skills Development',
        Target_Beneficiaries__c = 500,
        Funding_Goal__c = 250000,
        Start_Date__c = Date.today()
    ),
    new Programme__c(
        Name = 'Early Childhood Education - Eastern Cape',
        Status__c = 'Active',
        Province__c = 'Eastern Cape',
        Focus_Area__c = 'Early Childhood Education',
        Target_Beneficiaries__c = 300,
        Funding_Goal__c = 180000,
        Start_Date__c = Date.today()
    ),
    new Programme__c(
        Name = 'Women Economic Empowerment - KZN',
        Status__c = 'Active',
        Province__c = 'KwaZulu-Natal',
        Focus_Area__c = 'Women Economic Empowerment',
        Target_Beneficiaries__c = 200,
        Funding_Goal__c = 150000,
        Start_Date__c = Date.today()
    ),
    new Programme__c(
        Name = 'Rural Food Security - North West',
        Status__c = 'Active',
        Province__c = 'North West',
        Focus_Area__c = 'Rural Food Security',
        Target_Beneficiaries__c = 400,
        Funding_Goal__c = 200000,
        Start_Date__c = Date.today()
    ),
    new Programme__c(
        Name = 'Healthcare Access - Mpumalanga',
        Status__c = 'Active',
        Province__c = 'Mpumalanga',
        Focus_Area__c = 'Healthcare Access',
        Target_Beneficiaries__c = 350,
        Funding_Goal__c = 175000,
        Start_Date__c = Date.today()
    )
};
insert programmes;
System.debug('Programmes inserted: ' + programmes.size());

// Create donor Contacts
List<Contact> donors = new List<Contact>{
    new Contact(FirstName = 'Thabo', LastName = 'Nkosi'),
    new Contact(FirstName = 'Lerato', LastName = 'Dlamini'),
    new Contact(FirstName = 'Zanele', LastName = 'Mokoena'),
    new Contact(FirstName = 'Sipho', LastName = 'Mahlangu'),
    new Contact(FirstName = 'Nomsa', LastName = 'Zulu')
};
insert donors;
System.debug('Donors inserted: ' + donors.size());

// Create Donations
List<Donation__c> donations = new List<Donation__c>{
    new Donation__c(Programme__c = programmes[0].Id, Donor__c = donors[0].Id, Amount__c = 75000, Donation_Date__c = Date.today(), Payment_Method__c = 'EFT'),
    new Donation__c(Programme__c = programmes[0].Id, Donor__c = donors[1].Id, Amount__c = 50000, Donation_Date__c = Date.today(), Payment_Method__c = 'EFT'),
    new Donation__c(Programme__c = programmes[1].Id, Donor__c = donors[2].Id, Amount__c = 90000, Donation_Date__c = Date.today(), Payment_Method__c = 'Credit Card'),
    new Donation__c(Programme__c = programmes[1].Id, Donor__c = donors[3].Id, Amount__c = 45000, Donation_Date__c = Date.today(), Payment_Method__c = 'Debit Order'),
    new Donation__c(Programme__c = programmes[2].Id, Donor__c = donors[4].Id, Amount__c = 80000, Donation_Date__c = Date.today(), Payment_Method__c = 'EFT'),
    new Donation__c(Programme__c = programmes[2].Id, Donor__c = donors[0].Id, Amount__c = 15000, Donation_Date__c = Date.today(), Payment_Method__c = 'EFT'),
    new Donation__c(Programme__c = programmes[3].Id, Donor__c = donors[1].Id, Amount__c = 60000, Donation_Date__c = Date.today(), Payment_Method__c = 'EFT'),
    new Donation__c(Programme__c = programmes[4].Id, Donor__c = donors[2].Id, Amount__c = 55000, Donation_Date__c = Date.today(), Payment_Method__c = 'Credit Card')
};
insert donations;
System.debug('Donations inserted: ' + donations.size());

// Create Beneficiaries
List<Beneficiary__c> beneficiaries = new List<Beneficiary__c>{
    new Beneficiary__c(Name = 'Buhle Sithole', Programme__c = programmes[0].Id, Province__c = 'Limpopo', Age_Group__c = 'Youth (13-24)', Urban_Rural__c = 'Rural', Enrolment_Date__c = Date.today()),
    new Beneficiary__c(Name = 'Mpho Langa', Programme__c = programmes[0].Id, Province__c = 'Limpopo', Age_Group__c = 'Youth (13-24)', Urban_Rural__c = 'Rural', Enrolment_Date__c = Date.today()),
    new Beneficiary__c(Name = 'Thandeka Mthembu', Programme__c = programmes[0].Id, Province__c = 'Limpopo', Age_Group__c = 'Adult (25-59)', Urban_Rural__c = 'Rural', Enrolment_Date__c = Date.today()),
    new Beneficiary__c(Name = 'Lindiwe Dube', Programme__c = programmes[1].Id, Province__c = 'Eastern Cape', Age_Group__c = 'Child (0-12)', Urban_Rural__c = 'Rural', Enrolment_Date__c = Date.today()),
    new Beneficiary__c(Name = 'Ayanda Ntuli', Programme__c = programmes[1].Id, Province__c = 'Eastern Cape', Age_Group__c = 'Child (0-12)', Urban_Rural__c = 'Rural', Enrolment_Date__c = Date.today()),
    new Beneficiary__c(Name = 'Nompumelelo Khumalo', Programme__c = programmes[2].Id, Province__c = 'KwaZulu-Natal', Age_Group__c = 'Adult (25-59)', Urban_Rural__c = 'Urban', Enrolment_Date__c = Date.today()),
    new Beneficiary__c(Name = 'Fatima Cassim', Programme__c = programmes[2].Id, Province__c = 'KwaZulu-Natal', Age_Group__c = 'Adult (25-59)', Urban_Rural__c = 'Urban', Enrolment_Date__c = Date.today()),
    new Beneficiary__c(Name = 'Refilwe Tau', Programme__c = programmes[3].Id, Province__c = 'North West', Age_Group__c = 'Senior (60+)', Urban_Rural__c = 'Rural', Enrolment_Date__c = Date.today()),
    new Beneficiary__c(Name = 'Johannes Pretorius', Programme__c = programmes[3].Id, Province__c = 'North West', Age_Group__c = 'Adult (25-59)', Urban_Rural__c = 'Rural', Enrolment_Date__c = Date.today()),
    new Beneficiary__c(Name = 'Precious Shabangu', Programme__c = programmes[4].Id, Province__c = 'Mpumalanga', Age_Group__c = 'Adult (25-59)', Urban_Rural__c = 'Rural', Enrolment_Date__c = Date.today())
};
insert beneficiaries;
System.debug('Beneficiaries inserted: ' + beneficiaries.size());

System.debug('=== Seed data complete ===');
System.debug('Programmes: ' + programmes.size());
System.debug('Donors: ' + donors.size());
System.debug('Donations: ' + donations.size());
System.debug('Beneficiaries: ' + beneficiaries.size());