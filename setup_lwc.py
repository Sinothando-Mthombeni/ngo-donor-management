import os

files = {}

files["force-app/main/default/lwc/programmeDashboard/programmeDashboard.html"] = """<template>
    <lightning-card title="NGO Programme Dashboard" icon-name="standard:dashboard">
        <div class="slds-p-around_medium">

            <!-- Loading spinner -->
            <template if:true={isLoading}>
                <lightning-spinner alternative-text="Loading" size="medium"></lightning-spinner>
            </template>

            <template if:false={isLoading}>

                <!-- Error state -->
                <template if:true={hasError}>
                    <div class="slds-notify slds-notify_alert slds-alert_error">
                        <p>{errorMessage}</p>
                    </div>
                </template>

                <template if:false={hasError}>

                    <!-- Summary Stats Row -->
                    <div class="slds-grid slds-gutters slds-wrap slds-m-bottom_large">
                        <div class="slds-col slds-size_1-of-2 slds-medium-size_1-of-4">
                            <div class="slds-box slds-theme_shade slds-text-align_center">
                                <p class="slds-text-heading_large slds-text-color_success">{totalProgrammes}</p>
                                <p class="slds-text-body_small">Active Programmes</p>
                            </div>
                        </div>
                        <div class="slds-col slds-size_1-of-2 slds-medium-size_1-of-4">
                            <div class="slds-box slds-theme_shade slds-text-align_center">
                                <p class="slds-text-heading_large slds-text-color_success">{totalDonationsFormatted}</p>
                                <p class="slds-text-body_small">Total Donations</p>
                            </div>
                        </div>
                        <div class="slds-col slds-size_1-of-2 slds-medium-size_1-of-4">
                            <div class="slds-box slds-theme_shade slds-text-align_center">
                                <p class="slds-text-heading_large slds-text-color_success">{totalBeneficiaries}</p>
                                <p class="slds-text-body_small">Beneficiaries Enrolled</p>
                            </div>
                        </div>
                        <div class="slds-col slds-size_1-of-2 slds-medium-size_1-of-4">
                            <div class="slds-box slds-theme_shade slds-text-align_center">
                                <p class="slds-text-heading_large slds-text-color_success">{provincesReached}</p>
                                <p class="slds-text-body_small">Provinces Reached</p>
                            </div>
                        </div>
                    </div>

                    <!-- Programme Table -->
                    <h3 class="slds-text-heading_small slds-m-bottom_small">Programme Overview</h3>
                    <table class="slds-table slds-table_cell-buffer slds-table_bordered slds-table_striped">
                        <thead>
                            <tr class="slds-line-height_reset">
                                <th>Programme Name</th>
                                <th>Province</th>
                                <th>Focus Area</th>
                                <th>Status</th>
                                <th>Total Donations (ZAR)</th>
                                <th>Funding Progress</th>
                                <th>Beneficiaries</th>
                            </tr>
                        </thead>
                        <tbody>
                            <template for:each={programmes} for:item="prog">
                                <tr key={prog.Id}>
                                    <td>{prog.Name}</td>
                                    <td>{prog.Province__c}</td>
                                    <td>{prog.Focus_Area__c}</td>
                                    <td>
                                        <lightning-badge
                                            label={prog.Status__c}
                                            class={prog.statusClass}>
                                        </lightning-badge>
                                    </td>
                                    <td>R {prog.Total_Donations__c}</td>
                                    <td>
                                        <lightning-progress-bar
                                            value={prog.Funding_Progress__c}
                                            size="medium">
                                        </lightning-progress-bar>
                                        <span class="slds-text-body_small">{prog.Funding_Progress__c}%</span>
                                    </td>
                                    <td>{prog.BeneficiaryCount}</td>
                                </tr>
                            </template>
                        </tbody>
                    </table>

                    <!-- Province Breakdown -->
                    <h3 class="slds-text-heading_small slds-m-top_large slds-m-bottom_small">
                        Beneficiaries by Province
                    </h3>
                    <div class="slds-grid slds-gutters slds-wrap">
                        <template for:each={provinceStats} for:item="stat">
                            <div key={stat.province} class="slds-col slds-size_1-of-3 slds-m-bottom_small">
                                <div class="slds-box slds-theme_shade">
                                    <p class="slds-text-body_regular slds-text-color_default">
                                        <strong>{stat.province}</strong>
                                    </p>
                                    <p class="slds-text-body_small">{stat.count} beneficiaries</p>
                                    <lightning-progress-bar value={stat.percentage} size="small">
                                    </lightning-progress-bar>
                                </div>
                            </div>
                        </template>
                    </div>

                </template>
            </template>

        </div>
    </lightning-card>
</template>"""

files["force-app/main/default/lwc/programmeDashboard/programmeDashboard.js"] = """import { LightningElement, track, wire } from 'lwc';
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
}"""

files["force-app/main/default/lwc/programmeDashboard/programmeDashboard.css"] = """.slds-text-color_success {
    color: #2e7d32;
}

.slds-box {
    border-radius: 6px;
    padding: 12px;
}

table th {
    font-weight: 600;
    background-color: #f4f6f9;
}"""

files["force-app/main/default/lwc/programmeDashboard/programmeDashboard.js-meta.xml"] = """<?xml version="1.0" encoding="UTF-8"?>
<LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>62.0</apiVersion>
    <isExposed>true</isExposed>
    <targets>
        <target>lightning__AppPage</target>
        <target>lightning__HomePage</target>
        <target>lightning__RecordPage</target>
    </targets>
    <description>NGO Programme Dashboard showing donation totals, funding progress and beneficiary reach by province</description>
</LightningComponentBundle>"""

files["force-app/main/default/classes/ProgrammeDashboardController.cls"] = """/**
 * ProgrammeDashboardController
 *
 * Apex controller for the programmeDashboard LWC.
 * Returns all programmes with donation totals, funding progress,
 * and a map of beneficiary counts keyed by Programme Id.
 */
public with sharing class ProgrammeDashboardController {

    @AuraEnabled(cacheable=true)
    public static Map<String, Object> getDashboardData() {

        if (!Schema.sObjectType.Programme__c.isAccessible()) {
            throw new AuraHandledException(
                'Insufficient permissions to access Programme data.'
            );
        }

        // Query all programmes with calculated fields
        List<Programme__c> programmes = [
            SELECT Id,
                   Name,
                   Status__c,
                   Province__c,
                   Focus_Area__c,
                   Total_Donations__c,
                   Funding_Goal__c,
                   Funding_Progress__c,
                   Target_Beneficiaries__c,
                   Start_Date__c
            FROM Programme__c
            ORDER BY Province__c ASC, Name ASC
        ];

        // Query all beneficiaries for province breakdown
        List<Beneficiary__c> beneficiaries = [
            SELECT Id, Province__c, Programme__c, Urban_Rural__c
            FROM Beneficiary__c
        ];

        // Build beneficiary count map keyed by Programme Id
        Map<Id, Integer> beneficiaryCounts = new Map<Id, Integer>();
        for (Programme__c prog : programmes) {
            beneficiaryCounts.put(prog.Id, 0);
        }
        for (Beneficiary__c b : beneficiaries) {
            if (b.Programme__c != null && beneficiaryCounts.containsKey(b.Programme__c)) {
                beneficiaryCounts.put(
                    b.Programme__c,
                    beneficiaryCounts.get(b.Programme__c) + 1
                );
            }
        }

        // Return everything in one map — single callout from LWC
        Map<String, Object> result = new Map<String, Object>();
        result.put('programmes', programmes);
        result.put('beneficiaries', beneficiaries);
        result.put('beneficiaryCounts', beneficiaryCounts);

        return result;
    }
}"""

files["force-app/main/default/classes/ProgrammeDashboardController.cls-meta.xml"] = """<?xml version="1.0" encoding="UTF-8"?>
<ApexClass xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>62.0</apiVersion>
    <status>Active</status>
</ApexClass>"""

# Write all files
written = 0
for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content.strip())
    print(f"  Written: {path}")
    written += 1

print(f"\nDone — {written} files written successfully.")