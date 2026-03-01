import { LightningElement, track, wire } from 'lwc';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';
import getDashboardData from '@salesforce/apex/ProgrammeDashboardController.getDashboardData';

export default class ProgrammeDashboard extends LightningElement {

    @track programmes = [];
    @track provinceStats = [];
    @track isLoading = true;
    @track hasError = false;
    @track errorMessage = '';

    // Summary stat properties
    @track totalProgrammes = 0;
    @track totalDonationsFormatted = 'R0';
    @track totalBeneficiaries = 0;
    @track provincesReached = 0;

    @wire(getDashboardData)
    wiredData({ error, data }) {
        if (data) {
            this.processDashboardData(data);
            this.isLoading = false;
            this.hasError = false;
        } else if (error) {
            this.errorMessage = error.body ? error.body.message : 'Unknown error loading dashboard.';
            this.hasError = true;
            this.isLoading = false;
            this.showToast('Error', this.errorMessage, 'error');
        }
    }

    processDashboardData(data) {
        // Process programmes with derived display properties
        this.programmes = data.programmes.map(prog => ({
            ...prog,
            Funding_Progress__c: prog.Funding_Progress__c
                ? parseFloat((prog.Funding_Progress__c / 100).toFixed(1))
                : 0,
            BeneficiaryCount: data.beneficiaryCounts[prog.Id] || 0,
            statusClass: prog.Status__c === 'Active'
                ? 'slds-theme_success'
                : 'slds-theme_shade'
        }));

        // Summary stats
        this.totalProgrammes = this.programmes.filter(
            p => p.Status__c === 'Active'
        ).length;

        const totalDonations = this.programmes.reduce(
            (sum, p) => sum + (p.Total_Donations__c || 0), 0
        );
        this.totalDonationsFormatted = 'R' + totalDonations.toLocaleString('en-ZA', {
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        });

        this.totalBeneficiaries = Object.values(data.beneficiaryCounts).reduce(
            (sum, count) => sum + count, 0
        );

        // Province stats for breakdown section
        const provinceCounts = {};
        data.beneficiaries.forEach(b => {
            if (b.Province__c) {
                provinceCounts[b.Province__c] = (provinceCounts[b.Province__c] || 0) + 1;
            }
        });

        this.provincesReached = Object.keys(provinceCounts).length;

        const total = this.totalBeneficiaries || 1;
        this.provinceStats = Object.entries(provinceCounts)
            .map(([province, count]) => ({
                province,
                count,
                percentage: Math.round((count / total) * 100)
            }))
            .sort((a, b) => b.count - a.count);
    }

    showToast(title, message, variant) {
        this.dispatchEvent(new ShowToastEvent({ title, message, variant }));
    }
}