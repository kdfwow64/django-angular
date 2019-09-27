/*
Template Name: Color Admin - Responsive Admin Dashboard Template build with Twitter Bootstrap 3.3.7 & Bootstrap 4.0.0-Alpha 6
Version: 3.0.0
Author: Sean Ngu
Website: http://www.seantheme.com/color-admin-v3.0/admin/angularjs/
*/

var colorAdminApp = angular.module('colorAdminApp', [
    'ui.router',
    'ui.bootstrap',
    'oc.lazyLoad',
    'NgSwitchery',
    'ngFileUpload'
], function($interpolateProvider) {
    $interpolateProvider.startSymbol('{(');
    $interpolateProvider.endSymbol(')}');
});

colorAdminApp.config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/app/dashboard/v2');

    $stateProvider
        .state('app', {
            url: '/app',
            templateUrl: 'template/app.html',
            abstract: true
        })
        .state('app.dashboard', {
            url: '/dashboard',
            template: '<div ui-view></div>',
            abstract: true
        })
        .state('app.openitems', {
            url: '/openitems',
            template: '<div ui-view></div>',
            abstract: true
        })
        .state('app.openitems.evaluations', {
            url: '/evaluations',
            templateUrl: 'views/evaluations.html',
            data: { pageTitle: 'Evaluations' }
        })
        .state('app.openitems.reminders', {
            url: '/reminders',
            templateUrl: 'views/reminders.html',
            data: { pageTitle: 'Reminders' }
        })
        .state('app.openitems.tasks', {
            url: '/tasks',
            templateUrl: 'views/tasks.html',
            data: { pageTitle: 'Tasks' }
        })
        .state('app.openitems.completions', {
            url: '/completions',
            templateUrl: 'views/completions.html',
            data: { pageTitle: 'Completions' }
        })
        .state('app.meetings', {
            url: '/meetings',
            template: '<div ui-view></div>',
            abstract: true
        })
        .state('app.meetings.list_meetings', {
            url: '/list-meetings',
            templateUrl: 'views/list_meetings.html',
            data: { pageTitle: 'List Meetings' }
        })
        .state('app.meetings.create_meeting', {
            url: '/create-meeting',
            templateUrl: 'views/create_meeting.html',
            data: { pageTitle: 'Create Meeting' }
        })
        .state('app.meetings.search_meetings', {
            url: '/search-meeting',
            templateUrl: 'views/search_meeting.html',
            data: { pageTitle: 'Search Meeting' }
        })
        .state('app.calendar', {
            url: '/calendar',
            data: { pageTitle: 'Calendar' },
            templateUrl: 'views/calendar.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/fullcalendar/lib/moment.min.js',
                            '/static/dashboard_assets/plugins/fullcalendar/fullcalendar.min.css',
                            '/static/dashboard_assets/plugins/fullcalendar/fullcalendar.min.js'
                        ]
                    })
                }]
            }
        })
        .state('app.contacts', {
            url: '/contacts',
            template: '<div ui-view></div>',
            abstract: true
        })
        .state('app.contacts.list_contacts', {
            url: '/list-contacts',
            templateUrl: 'views/list_contacts.html',
            data: { pageTitle: 'List Contacts' }
        })
        .state('app.entries', {
            url: '/entries',
            template: '<div ui-view></div>',
            abstract: true
        })
        .state('app.entries.list_entries', {
            url: '/list-entries',
            templateUrl: 'views/list_entries.html',
            data: { pageTitle: 'List Entries' },
            controller: 'registerListEntriesController',
            resolve: {
                responses: function(ResponseService){
                    return ResponseService.getAllResponses();
                },
                severities: function(SeverityService){
                    return SeverityService.getAllSeverities();
                },
                users: function(UserService){
                    return UserService.getUsers();
                },
                // users: function(UserService){
                //     return UserService.getUsers();
                // },
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/DataTables/media/css/dataTables.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/css/responsive.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/media/js/jquery.dataTables.js',
                            '/static/dashboard_assets/plugins/DataTables/media/js/dataTables.bootstrap.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/js/dataTables.responsive.min.js',
                        ]
                    });
                }]
            }
        })
        .state('app.entries.add_entry', {
            url: '/add-entry',
            templateUrl: 'views/add_entry.html',
            data: { pageTitle: 'Add Entry' },
            controller: 'registerAddEntriesController',
            resolve: {
                riskTypes: function(RiskTypeService){
                    return RiskTypeService.getAllMyRiskTypes();
                },
                responses: function(ResponseService){
                    return ResponseService.getAllResponses();
                },
                companyLocations: function(CompanyLocationService){
                    return CompanyLocationService.getCompanyLocations();
                },
                compliances: function(ComplianceService){
                    return ComplianceService.getCompliances();
                },
                users: function(UserService){
                    return UserService.getUsers();
                },
                actors: function(ActorService){
                    return ActorService.getActors();
                },
                actorIntents: function(ActorIntentService){
                    return ActorIntentService.getActorIntents();
                },
                actorMotives: function(ActorMotiveService){
                    return ActorMotiveService.getActorMotives();
                },
                companyAssets: function(CompanyAssetsService){
                    return CompanyAssetsService.getCompanyAssets();
                },
                ancillaryItemTypes: function(AncillaryItemsService){
                    return AncillaryItemsService.getAncillaryItems();
                },
                companyControls: function(CompanyControlsService){
                    return CompanyControlsService.getCompanyControls();
                },
                controlMeasures: function(CompanyControlMeasuresService){
                    return CompanyControlMeasuresService.getCompanyControlMeasures();
                },
                riskEntry: function($stateParams, RiskEntryService){
                    return RiskEntryService.getselectedRiskEntry(0);
                },
                aro_time_units: function(TimeUnitService){
                    return TimeUnitService.getAllTimeUnits();
                },
                aro_frequencies: function(FrequencyCategoryService){
                    return FrequencyCategoryService.getAllFrequencies();
                },
                artifacts: function(EntryUrlService){
                    return EntryUrlService.getAllEntryUrls();
                },
                compliance_types: function(ComplianceTypeService){
                    return ComplianceTypeService.getAllComplianceTypes();
                },
                severities: function(SeverityService){
                    return SeverityService.getAllSeverities();
                },
                current_company_max_loss: function(CompanyService){
                    return CompanyService.getCompanyMaxLoss();
                },
                frequencies: function(FrequencyCategoryService){
                    return FrequencyCategoryService.getAllFrequencies();
                },
                severity_categories: function(SeverityService){
                    return SeverityService.getAllSeverities();
                },
                impact_categories: function(ImpactCategoryService){
                    return ImpactCategoryService.getAllImpactCategories();
                },
                financial_detail: function(FinancialDetailService){
                    return FinancialDetailService.getFinancialDetail();
                },
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/bootstrap-wizard/css/bwizard.min.css',
                            '/static/dashboard_assets/plugins/parsley/src/parsley.css',
                            '/static/dashboard_assets/plugins/pace/pace.min.js',
                            '/static/dashboard_assets/plugins/parsley/dist/parsley.min.js',
                            '/static/dashboard_assets/plugins/bootstrap-wizard/js/bwizard.js',
                        ]
                    });
                }]
            }
        })
        .state('app.entries.edit_entry', {
            url: '/edit-entry/:id',
            templateUrl: 'views/add_entry.html',
            data: { pageTitle: 'Edit Entry' },
            controller: 'registerAddEntriesController',
            resolve: {
                riskTypes: function(RiskTypeService){
                    return RiskTypeService.getAllMyRiskTypes();
                },
                responses: function(ResponseService){
                    return ResponseService.getAllResponses();
                },
                companyLocations: function(CompanyLocationService){
                    return CompanyLocationService.getCompanyLocations();
                },
                compliances: function(ComplianceService){
                    return ComplianceService.getCompliances();
                },
                users: function(UserService){
                    return UserService.getUsers();
                },
                actors: function(ActorService){
                    return ActorService.getActors();
                },
                actorIntents: function(ActorIntentService){
                    return ActorIntentService.getActorIntents();
                },
                actorMotives: function(ActorMotiveService){
                    return ActorMotiveService.getActorMotives();
                },
                companyAssets: function(CompanyAssetsService){
                    return CompanyAssetsService.getCompanyAssets();
                },
                ancillaryItemTypes: function(AncillaryItemsService){
                    return AncillaryItemsService.getAncillaryItems();
                },
                companyControls: function(CompanyControlsService){
                    return CompanyControlsService.getCompanyControls();
                },
                controlMeasures: function(CompanyControlMeasuresService){
                    return CompanyControlMeasuresService.getCompanyControlMeasures();
                },
                riskEntry: function($stateParams, RiskEntryService){
                    return RiskEntryService.getselectedRiskEntry($stateParams.id);
                },
                aro_time_units: function(TimeUnitService){
                    return TimeUnitService.getAllTimeUnits();
                },
                aro_frequencies: function(FrequencyCategoryService){
                    return FrequencyCategoryService.getAllFrequencies();
                },
                artifacts: function(EntryUrlService){
                    return EntryUrlService.getAllEntryUrls();
                },
                compliance_types: function(ComplianceTypeService){
                    return ComplianceTypeService.getAllComplianceTypes();
                },
                severities: function(SeverityService){
                    return SeverityService.getAllSeverities();
                },
                current_company_max_loss: function(CompanyService){
                    return CompanyService.getCompanyMaxLoss();
                },
                frequencies: function(FrequencyCategoryService){
                    return FrequencyCategoryService.getAllFrequencies();
                },
                severity_categories: function(SeverityService){
                    return SeverityService.getAllSeverities();
                },
                impact_categories: function(ImpactCategoryService){
                    return ImpactCategoryService.getAllImpactCategories();
                },
                financial_detail: function(FinancialDetailService){
                    return FinancialDetailService.getFinancialDetail();
                },
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/bootstrap-wizard/css/bwizard.min.css',
                            '/static/dashboard_assets/plugins/parsley/src/parsley.css',
                            '/static/dashboard_assets/plugins/pace/pace.min.js',
                            '/static/dashboard_assets/plugins/parsley/dist/parsley.min.js',
                            '/static/dashboard_assets/plugins/bootstrap-wizard/js/bwizard.js',
                        ]
                    });
                }]
            }
        })
        .state('app.entries.edit_entry_show_mitigation', {
            url: '/edit-entry-show-mitigation/:id',
            templateUrl: 'views/add_entry.html',
            data: { pageTitle: 'Edit Entry' },
            controller: 'registerAddEntriesController',
            resolve: {
                riskTypes: function(RiskTypeService){
                    return RiskTypeService.getAllMyRiskTypes();
                },
                responses: function(ResponseService){
                    return ResponseService.getAllResponses();
                },
                companyLocations: function(CompanyLocationService){
                    return CompanyLocationService.getCompanyLocations();
                },
                compliances: function(ComplianceService){
                    return ComplianceService.getCompliances();
                },
                users: function(UserService){
                    return UserService.getUsers();
                },
                actors: function(ActorService){
                    return ActorService.getActors();
                },
                actorIntents: function(ActorIntentService){
                    return ActorIntentService.getActorIntents();
                },
                actorMotives: function(ActorMotiveService){
                    return ActorMotiveService.getActorMotives();
                },
                companyAssets: function(CompanyAssetsService){
                    return CompanyAssetsService.getCompanyAssets();
                },
                ancillaryItemTypes: function(AncillaryItemsService){
                    return AncillaryItemsService.getAncillaryItems();
                },
                companyControls: function(CompanyControlsService){
                    return CompanyControlsService.getCompanyControls();
                },
                controlMeasures: function(CompanyControlMeasuresService){
                    return CompanyControlMeasuresService.getCompanyControlMeasures();
                },
                riskEntry: function($stateParams, RiskEntryService){
                    return RiskEntryService.getselectedRiskEntry($stateParams.id);
                },
                aro_time_units: function(TimeUnitService){
                    return TimeUnitService.getAllTimeUnits();
                },
                aro_frequencies: function(FrequencyCategoryService){
                    return FrequencyCategoryService.getAllFrequencies();
                },
                artifacts: function(EntryUrlService){
                    return EntryUrlService.getAllEntryUrls();
                },
                compliance_types: function(ComplianceTypeService){
                    return ComplianceTypeService.getAllComplianceTypes();
                },
                severities: function(SeverityService){
                    return SeverityService.getAllSeverities();
                },
                current_company_max_loss: function(CompanyService){
                    return CompanyService.getCompanyMaxLoss();
                },
                frequencies: function(FrequencyCategoryService){
                    return FrequencyCategoryService.getAllFrequencies();
                },
                severity_categories: function(SeverityService){
                    return SeverityService.getAllSeverities();
                },
                impact_categories: function(ImpactCategoryService){
                    return ImpactCategoryService.getAllImpactCategories();
                },
                financial_detail: function(FinancialDetailService){
                    return FinancialDetailService.getFinancialDetail();
                },
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/bootstrap-wizard/css/bwizard.min.css',
                            '/static/dashboard_assets/plugins/parsley/src/parsley.css',
                            '/static/dashboard_assets/plugins/pace/pace.min.js',
                            '/static/dashboard_assets/plugins/parsley/dist/parsley.min.js',
                            '/static/dashboard_assets/plugins/bootstrap-wizard/js/bwizard.js',
                        ]
                    });
                }]
            }
        })
        .state('app.entries.edit_entry_show_assets', {
            url: '/edit-entry-show-assets/:id',
            templateUrl: 'views/add_entry.html',
            data: { pageTitle: 'Edit Entry' },
            controller: 'registerAddEntriesController',
            resolve: {
                riskTypes: function(RiskTypeService){
                    return RiskTypeService.getAllMyRiskTypes();
                },
                responses: function(ResponseService){
                    return ResponseService.getAllResponses();
                },
                companyLocations: function(CompanyLocationService){
                    return CompanyLocationService.getCompanyLocations();
                },
                compliances: function(ComplianceService){
                    return ComplianceService.getCompliances();
                },
                users: function(UserService){
                    return UserService.getUsers();
                },
                actors: function(ActorService){
                    return ActorService.getActors();
                },
                actorIntents: function(ActorIntentService){
                    return ActorIntentService.getActorIntents();
                },
                actorMotives: function(ActorMotiveService){
                    return ActorMotiveService.getActorMotives();
                },
                companyAssets: function(CompanyAssetsService){
                    return CompanyAssetsService.getCompanyAssets();
                },
                ancillaryItemTypes: function(AncillaryItemsService){
                    return AncillaryItemsService.getAncillaryItems();
                },
                companyControls: function(CompanyControlsService){
                    return CompanyControlsService.getCompanyControls();
                },
                controlMeasures: function(CompanyControlMeasuresService){
                    return CompanyControlMeasuresService.getCompanyControlMeasures();
                },
                riskEntry: function($stateParams, RiskEntryService){
                    return RiskEntryService.getselectedRiskEntry($stateParams.id);
                },
                aro_time_units: function(TimeUnitService){
                    return TimeUnitService.getAllTimeUnits();
                },
                aro_frequencies: function(FrequencyCategoryService){
                    return FrequencyCategoryService.getAllFrequencies();
                },
                artifacts: function(EntryUrlService){
                    return EntryUrlService.getAllEntryUrls();
                },
                compliance_types: function(ComplianceTypeService){
                    return ComplianceTypeService.getAllComplianceTypes();
                },
                severities: function(SeverityService){
                    return SeverityService.getAllSeverities();
                },
                current_company_max_loss: function(CompanyService){
                    return CompanyService.getCompanyMaxLoss();
                },
                frequencies: function(FrequencyCategoryService){
                    return FrequencyCategoryService.getAllFrequencies();
                },
                severity_categories: function(SeverityService){
                    return SeverityService.getAllSeverities();
                },
                impact_categories: function(ImpactCategoryService){
                    return ImpactCategoryService.getAllImpactCategories();
                },
                financial_detail: function(FinancialDetailService){
                    return FinancialDetailService.getFinancialDetail();
                },

                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/bootstrap-wizard/css/bwizard.min.css',
                            '/static/dashboard_assets/plugins/parsley/src/parsley.css',
                            '/static/dashboard_assets/plugins/pace/pace.min.js',
                            '/static/dashboard_assets/plugins/parsley/dist/parsley.min.js',
                            '/static/dashboard_assets/plugins/bootstrap-wizard/js/bwizard.js',
                        ]
                    });
                }]
            }
        })
        .state('app.controls', {
            url: '/controls',
            template: '<div ui-view></div>',
            abstract: true
        })
        .state('app.controls.list_controls', {
            url: '/list-controls',
            templateUrl: 'views/list_controls.html',
            data: { pageTitle: 'List Controls' },
            controller: 'CompanyControlListController',
            resolve: {
                company_contacts: function(CompanyContactService){
                    return CompanyContactService.getAllCompanyContact();
                },
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/bootstrap-wizard/css/bwizard.min.css',
                            '/static/dashboard_assets/plugins/parsley/src/parsley.css',
                            '/static/dashboard_assets/plugins/pace/pace.min.js',
                            '/static/dashboard_assets/plugins/parsley/dist/parsley.min.js',
                            '/static/dashboard_assets/plugins/bootstrap-wizard/js/bwizard.js',
                            '/static/dashboard_assets/plugins/DataTables/media/css/dataTables.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/css/responsive.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/media/js/jquery.dataTables.js',
                            '/static/dashboard_assets/plugins/DataTables/media/js/dataTables.bootstrap.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/js/dataTables.responsive.min.js'
                        ]
                    });
                }]
            }
        })
        .state('app.controls.control_check_in', {
            url: '/control-check-in',
            templateUrl: 'views/control_check_in.html',
            data: { pageTitle: 'Control Check-In' },
            controller: 'registerControlCheckInController',
            resolve: {
                locations: function(CompanyLocationService){
                    return CompanyLocationService.getCompanyLocations();
                },
                segments: function(CompanySegmentService){
                    return CompanySegmentService.getCompanySegments();
                },
                recovery_time_units: function(TimeUnitService){
                    return TimeUnitService.getAllTimeUnits();
                },
                control_categories: function(ControlCategoryService){
                    return ControlCategoryService.getAllControlCategories();
                },
                company_contacts: function(CompanyContactService){
                    return CompanyContactService.getAllCompanyContact();
                },
                company_control: function($stateParams, CompanyControlService){
                    return CompanyControlService.getSelectedCompanyControl(0);
                },
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/bootstrap-wizard/css/bwizard.min.css',
                            '/static/dashboard_assets/plugins/parsley/src/parsley.css',
                            '/static/dashboard_assets/plugins/pace/pace.min.js',
                            '/static/dashboard_assets/plugins/parsley/dist/parsley.min.js',
                            '/static/dashboard_assets/plugins/bootstrap-wizard/js/bwizard.js',
                            '/static/dashboard_assets/plugins/DataTables/media/css/dataTables.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/css/responsive.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/media/js/jquery.dataTables.js',
                            '/static/dashboard_assets/plugins/DataTables/media/js/dataTables.bootstrap.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/js/dataTables.responsive.min.js'
                        ]
                    });
                }]
            }
        })
        .state('app.controls.edit_company_control', {
            url: '/edit-company-control/:id',
            templateUrl: 'views/control_check_in.html',
            data: { pageTitle: 'Edit Company Control' },
            controller: 'registerControlCheckInController',
            resolve: {
                locations: function(CompanyLocationService){
                    return CompanyLocationService.getCompanyLocations();
                },
                segments: function(CompanySegmentService){
                    return CompanySegmentService.getCompanySegments();
                },
                recovery_time_units: function(TimeUnitService){
                    return TimeUnitService.getAllTimeUnits();
                },
                control_categories: function(ControlCategoryService){
                    return ControlCategoryService.getAllControlCategories();
                },
                company_contacts: function(CompanyContactService){
                    return CompanyContactService.getAllCompanyContact();
                },
                company_control: function($stateParams, CompanyControlService){
                    return CompanyControlService.getSelectedCompanyControl($stateParams.id);
                },
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/bootstrap-wizard/css/bwizard.min.css',
                            '/static/dashboard_assets/plugins/parsley/src/parsley.css',
                            '/static/dashboard_assets/plugins/pace/pace.min.js',
                            '/static/dashboard_assets/plugins/parsley/dist/parsley.min.js',
                            '/static/dashboard_assets/plugins/bootstrap-wizard/js/bwizard.js',
                            '/static/dashboard_assets/plugins/DataTables/media/css/dataTables.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/css/responsive.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/media/js/jquery.dataTables.js',
                            '/static/dashboard_assets/plugins/DataTables/media/js/dataTables.bootstrap.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/js/dataTables.responsive.min.js'
                        ]
                    });
                }]
            }
        })
        .state('app.assets.add_company_asset', {
            url: '/add-company-asset',
            templateUrl: 'views/add_company_asset.html',
            data: { pageTitle: 'Add Company Asset' },
            controller: 'registerAddCompanyAssetController',
            resolve: {
                company_asset_types: function(CompanyAssetTypeService){
                    return CompanyAssetTypeService.getAllCompanyAssetType();
                },
                locations: function(CompanyLocationService){
                    return CompanyLocationService.getCompanyLocations();
                },
                company_asset_owners: function(CompanyContactService){
                    return CompanyContactService.getAllCompanyContact();
                },
                time_units: function(TimeUnitService){
                    return TimeUnitService.getAllTimeUnits();
                },
                annual_revenue: function(CompanyDetailService){
                    return CompanyDetailService.getCompanyAnnualRevenue();
                },
                CompanyAsset: function($stateParams, CompanyAssetService){
                    return CompanyAssetService.getSelectedCompanyAsset(0);
                },
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/bootstrap-wizard/css/bwizard.min.css',
                            '/static/dashboard_assets/plugins/parsley/src/parsley.css',
                            '/static/dashboard_assets/plugins/pace/pace.min.js',
                            '/static/dashboard_assets/plugins/parsley/dist/parsley.min.js',
                            '/static/dashboard_assets/plugins/bootstrap-wizard/js/bwizard.js'
                        ]
                    });
                }]
            }
        })
        .state('app.assets.edit_company_asset', {
            url: '/edit-company-asset/:id',
            templateUrl: 'views/add_company_asset.html',
            data: { pageTitle: 'Edit Company Asset' },
            controller: 'registerAddCompanyAssetController',
            resolve: {
                company_asset_types: function(CompanyAssetTypeService){
                    return CompanyAssetTypeService.getAllCompanyAssetType();
                },
                locations: function(CompanyLocationService){
                    return CompanyLocationService.getCompanyLocations();
                },
                company_asset_owners: function(CompanyContactService){
                    return CompanyContactService.getAllCompanyContact();
                },
                time_units: function(TimeUnitService){
                    return TimeUnitService.getAllTimeUnits();
                },
                annual_revenue: function(CompanyDetailService){
                    return CompanyDetailService.getCompanyAnnualRevenue();
                },
                CompanyAsset: function($stateParams, CompanyAssetService){
                    return CompanyAssetService.getSelectedCompanyAsset($stateParams.id);
                },
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/bootstrap-wizard/css/bwizard.min.css',
                            '/static/dashboard_assets/plugins/parsley/src/parsley.css',
                            '/static/dashboard_assets/plugins/pace/pace.min.js',
                            '/static/dashboard_assets/plugins/parsley/dist/parsley.min.js',
                            '/static/dashboard_assets/plugins/bootstrap-wizard/js/bwizard.js'
                        ]
                    });
                }]
            }
        })
        .state('app.controls.list_control_groups', {
            url: '/list-control-groups',
            templateUrl: 'views/list_control_groups.html',
            data: { pageTitle: 'Company Control Groups' },
            // resolve: {
            //     service: ['$ocLazyLoad', function($ocLazyLoad) {
            //         return $ocLazyLoad.load({
            //             serie: true,
            //             files: [
            //                 '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap.css',
            //                 '/static/dashboard_assets/plugins/bootstrap-calendar/css/bootstrap_calendar.css',
            //                 '/static/dashboard_assets/plugins/gritter/css/jquery.gritter.css',
            //                 '/static/dashboard_assets/plugins/morris/morris.css',
            //                 '/static/dashboard_assets/plugins/morris/raphael.min.js',
            //                 '/static/dashboard_assets/plugins/morris/morris.js',
            //                 '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap.min.js',
            //                 '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap-world-merc-en.js',
            //                 '/static/dashboard_assets/plugins/bootstrap-calendar/js/bootstrap_calendar.min.js',
            //                 '/static/dashboard_assets/plugins/gritter/js/jquery.gritter.js'
            //             ]
            //         });
            //     }]
            // }
        })
        .state('app.controls.control_category_list', {
            url: '/control-category-list',
            templateUrl: 'views/list_control_category.html',
            data: { pageTitle: 'Control Category Lookup' },
            // resolve: {
            //     service: ['$ocLazyLoad', function($ocLazyLoad) {
            //         return $ocLazyLoad.load({
            //             serie: true,
            //             files: [
            //                 '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap.css',
            //                 '/static/dashboard_assets/plugins/bootstrap-calendar/css/bootstrap_calendar.css',
            //                 '/static/dashboard_assets/plugins/gritter/css/jquery.gritter.css',
            //                 '/static/dashboard_assets/plugins/morris/morris.css',
            //                 '/static/dashboard_assets/plugins/morris/raphael.min.js',
            //                 '/static/dashboard_assets/plugins/morris/morris.js',
            //                 '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap.min.js',
            //                 '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap-world-merc-en.js',
            //                 '/static/dashboard_assets/plugins/bootstrap-calendar/js/bootstrap_calendar.min.js',
            //                 '/static/dashboard_assets/plugins/gritter/js/jquery.gritter.js'
            //             ]
            //         });
            //     }]
            // }
        })
        .state('app.assets', {
            url: '/assets',
            template: '<div ui-view></div>',
            abstract: true
        })
        .state('app.assets.list_assets', {
            url: '/list-assets',
            templateUrl: 'views/list_assets.html',
            data: { pageTitle: 'List Assets' },
            controller: 'CompanyAssetListController',
            resolve: {
                company_contacts: function(CompanyContactService){
                    return CompanyContactService.getAllCompanyContact();
                },
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/bootstrap-wizard/css/bwizard.min.css',
                            '/static/dashboard_assets/plugins/parsley/src/parsley.css',
                            '/static/dashboard_assets/plugins/pace/pace.min.js',
                            '/static/dashboard_assets/plugins/parsley/dist/parsley.min.js',
                            '/static/dashboard_assets/plugins/bootstrap-wizard/js/bwizard.js',
                            '/static/dashboard_assets/plugins/DataTables/media/css/dataTables.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/css/responsive.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/media/js/jquery.dataTables.js',
                            '/static/dashboard_assets/plugins/DataTables/media/js/dataTables.bootstrap.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/js/dataTables.responsive.min.js'
                        ]
                    });
                }]
            }
        })
        .state('app.vendors', {
            url: '/vendors',
            template: '<div ui-view></div>',
            abstract: true
        })
        .state('app.vendors.list_vendors', {
            url: '/list-vendors',
            templateUrl: 'views/list_vendors.html',
            data: { pageTitle: 'List Vendors' },
            // resolve: {
            //     service: ['$ocLazyLoad', function($ocLazyLoad) {
            //         return $ocLazyLoad.load({
            //             serie: true,
            //             files: [
            //                 '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap.css',
            //                 '/static/dashboard_assets/plugins/bootstrap-calendar/css/bootstrap_calendar.css',
            //                 '/static/dashboard_assets/plugins/gritter/css/jquery.gritter.css',
            //                 '/static/dashboard_assets/plugins/morris/morris.css',
            //                 '/static/dashboard_assets/plugins/morris/raphael.min.js',
            //                 '/static/dashboard_assets/plugins/morris/morris.js',
            //                 '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap.min.js',
            //                 '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap-world-merc-en.js',
            //                 '/static/dashboard_assets/plugins/bootstrap-calendar/js/bootstrap_calendar.min.js',
            //                 '/static/dashboard_assets/plugins/gritter/js/jquery.gritter.js'
            //             ]
            //         });
            //     }]
            // }
        })
        .state('app.projects', {
            url: '/projects',
            template: '<div ui-view></div>',
            abstract: true
        })
        .state('app.projects.list_projects', {
            url: '/list-projects',
            templateUrl: 'views/list_projects.html',
            data: { pageTitle: 'List Projects' },
            // resolve: {
            //     service: ['$ocLazyLoad', function($ocLazyLoad) {
            //         return $ocLazyLoad.load({
            //             serie: true,
            //             files: [
            //                 '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap.css',
            //                 '/static/dashboard_assets/plugins/bootstrap-calendar/css/bootstrap_calendar.css',
            //                 '/static/dashboard_assets/plugins/gritter/css/jquery.gritter.css',
            //                 '/static/dashboard_assets/plugins/morris/morris.css',
            //                 '/static/dashboard_assets/plugins/morris/raphael.min.js',
            //                 '/static/dashboard_assets/plugins/morris/morris.js',
            //                 '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap.min.js',
            //                 '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap-world-merc-en.js',
            //                 '/static/dashboard_assets/plugins/bootstrap-calendar/js/bootstrap_calendar.min.js',
            //                 '/static/dashboard_assets/plugins/gritter/js/jquery.gritter.js'
            //             ]
            //         });
            //     }]
            // }
        })
        .state('app.projects.add_project', {
            url: '/add-project',
            templateUrl: 'views/add_project.html',
            data: { pageTitle: 'Add Project' },
            // resolve: {
            //     service: ['$ocLazyLoad', function($ocLazyLoad) {
            //         return $ocLazyLoad.load({
            //             serie: true,
            //             files: [
            //                 '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap.css',
            //                 '/static/dashboard_assets/plugins/bootstrap-calendar/css/bootstrap_calendar.css',
            //                 '/static/dashboard_assets/plugins/gritter/css/jquery.gritter.css',
            //                 '/static/dashboard_assets/plugins/morris/morris.css',
            //                 '/static/dashboard_assets/plugins/morris/raphael.min.js',
            //                 '/static/dashboard_assets/plugins/morris/morris.js',
            //                 '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap.min.js',
            //                 '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap-world-merc-en.js',
            //                 '/static/dashboard_assets/plugins/bootstrap-calendar/js/bootstrap_calendar.min.js',
            //                 '/static/dashboard_assets/plugins/gritter/js/jquery.gritter.js'
            //             ]
            //         });
            //     }]
            // }
        })
        .state('app.playbooks', {
            url: '/playbooks',
            template: '<div ui-view></div>',
            abstract: true
        })
        .state('app.playbooks.list_playbooks', {
            url: '/list-playbooks',
            templateUrl: 'views/list_playbooks.html',
            data: { pageTitle: 'List Playbooks' },
            // resolve: {
            //     service: ['$ocLazyLoad', function($ocLazyLoad) {
            //         return $ocLazyLoad.load({
            //             serie: true,
            //             files: [
            //                 '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap.css',
            //                 '/static/dashboard_assets/plugins/bootstrap-calendar/css/bootstrap_calendar.css',
            //                 '/static/dashboard_assets/plugins/gritter/css/jquery.gritter.css',
            //                 '/static/dashboard_assets/plugins/morris/morris.css',
            //                 '/static/dashboard_assets/plugins/morris/raphael.min.js',
            //                 '/static/dashboard_assets/plugins/morris/morris.js',
            //                 '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap.min.js',
            //                 '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap-world-merc-en.js',
            //                 '/static/dashboard_assets/plugins/bootstrap-calendar/js/bootstrap_calendar.min.js',
            //                 '/static/dashboard_assets/plugins/gritter/js/jquery.gritter.js'
            //             ]
            //         });
            //     }]
            // }
        })
        .state('app.playbooks.create_playbook', {
            url: '/create-playbook',
            templateUrl: 'views/create_playbook.html',
            data: { pageTitle: 'Create Playbook' },
            // resolve: {
            //     service: ['$ocLazyLoad', function($ocLazyLoad) {
            //         return $ocLazyLoad.load({
            //             serie: true,
            //             files: [
            //                 '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap.css',
            //                 '/static/dashboard_assets/plugins/bootstrap-calendar/css/bootstrap_calendar.css',
            //                 '/static/dashboard_assets/plugins/gritter/css/jquery.gritter.css',
            //                 '/static/dashboard_assets/plugins/morris/morris.css',
            //                 '/static/dashboard_assets/plugins/morris/raphael.min.js',
            //                 '/static/dashboard_assets/plugins/morris/morris.js',
            //                 '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap.min.js',
            //                 '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap-world-merc-en.js',
            //                 '/static/dashboard_assets/plugins/bootstrap-calendar/js/bootstrap_calendar.min.js',
            //                 '/static/dashboard_assets/plugins/gritter/js/jquery.gritter.js'
            //             ]
            //         });
            //     }]
            // }
        })
        .state('app.dashboard.v1', {
            url: '/v1',
            templateUrl: 'views/index.html',
            data: { pageTitle: 'Dashboard v1' },
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap.css',
                            '/static/dashboard_assets/plugins/bootstrap-datepicker/css/bootstrap-datepicker.css',
                            '/static/dashboard_assets/plugins/gritter/css/jquery.gritter.css',
                            '/static/dashboard_assets/plugins/gritter/js/jquery.gritter.js',
                            '/static/dashboard_assets/plugins/flot/jquery.flot.min.js',
                            '/static/dashboard_assets/plugins/flot/jquery.flot.time.min.js',
                            '/static/dashboard_assets/plugins/flot/jquery.flot.resize.min.js',
                            '/static/dashboard_assets/plugins/flot/jquery.flot.pie.min.js',
                            '/static/dashboard_assets/plugins/sparkline/jquery.sparkline.js',
                            '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap.min.js',
                            '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap-world-mill-en.js',
                            '/static/dashboard_assets/plugins/bootstrap-datepicker/js/bootstrap-datepicker.js'
                        ]
                    });
                }]
            }
        })
        .state('app.dashboard.v2', {
            url: '/v2',
            templateUrl: 'views/index_v2.html',
            data: { pageTitle: 'Risk Log Book' },
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap.css',
                            '/static/dashboard_assets/plugins/bootstrap-calendar/css/bootstrap_calendar.css',
                            '/static/dashboard_assets/plugins/gritter/css/jquery.gritter.css',
                            '/static/dashboard_assets/plugins/morris/morris.css',
                            '/static/dashboard_assets/plugins/morris/raphael.min.js',
                            '/static/dashboard_assets/plugins/morris/morris.js',
                            '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap.min.js',
                            '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap-world-merc-en.js',
                            '/static/dashboard_assets/plugins/bootstrap-calendar/js/bootstrap_calendar.min.js',
                            '/static/dashboard_assets/plugins/gritter/js/jquery.gritter.js'
                        ]
                    });
                }]
            }
        })
        .state('app.email', {
            url: '/email',
            template: '<div ui-view></div>',
            abstract: true
        })
        .state('app.email.inbox', {
            url: '/inbox/v1',
            data: { pageTitle: 'Email Inbox v1' },
            templateUrl: 'views/email_inbox.html'
        })
        .state('app.email.inbox-v2', {
            url: '/inbox/v2',
            data: { pageTitle: 'Email Inbox v2' },
            templateUrl: 'views/email_inbox_v2.html'
        })
        .state('app.email.compose', {
            url: '/compose',
            data: { pageTitle: 'Email Compose' },
            templateUrl: 'views/email_compose.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/jquery-tag-it/css/jquery.tagit.css',
                            '/static/dashboard_assets/plugins/bootstrap-wysihtml5/src/bootstrap-wysihtml5.css',
                            '/static/dashboard_assets/plugins/jquery-tag-it/js/tag-it.min.js',
                            '/static/dashboard_assets/plugins/bootstrap-wysihtml5/lib/js/wysihtml5-0.3.0.js',
                            '/static/dashboard_assets/plugins/bootstrap-wysihtml5/src/bootstrap-wysihtml5.js'
                        ]
                    })
                }]
            }
        })
        .state('app.email.detail', {
            url: '/detail',
            data: { pageTitle: 'Email Detail' },
            templateUrl: 'views/email_detail.html'
        })
        /*.state('app.ui', {
            url: '/ui',
            template: '<div ui-view></div>',
            abstract: true
        })
        .state('app.ui.general', {
            url: '/general',
            data: { pageTitle: 'UI General' },
            templateUrl: 'views/ui_general.html'
        })
        .state('app.ui.typography', {
            url: '/typography',
            data: { pageTitle: 'UI Typography' },
            templateUrl: 'views/ui_typography.html'
        })
        .state('app.ui.tabsAccordions', {
            url: '/tabs-accordions',
            data: { pageTitle: 'UI Tabs & Accordions' },
            templateUrl: 'views/ui_tabs_accordions.html'
        })
        .state('app.ui.unlimitedTabs', {
            url: '/unlimited-nav-tabs',
            data: { pageTitle: 'UI Unlimited Nav Tabs' },
            templateUrl: 'views/ui_unlimited_tabs.html'
        })
        .state('app.ui.modalNotification', {
            url: '/modal-notification',
            data: { pageTitle: 'UI Modal & Notification' },
            templateUrl: 'views/ui_modal_notification.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        files: [
                            '/static/dashboard_assets/plugins/gritter/css/jquery.gritter.css',
                            '/static/dashboard_assets/plugins/gritter/js/jquery.gritter.js',
                            '/static/dashboard_assets/plugins/bootstrap-sweetalert/sweetalert.css',
                            '/static/dashboard_assets/plugins/bootstrap-sweetalert/sweetalert.min.js'
                        ]
                    });
                }]
            }
        })
        .state('app.ui.widgetBoxes', {
            url: '/widget-boxes',
            data: { pageTitle: 'UI Widget Boxes' },
            templateUrl: 'views/ui_widget_boxes.html'
        })
        .state('app.ui.mediaObject', {
            url: '/media-object',
            data: { pageTitle: 'UI Media Object' },
            templateUrl: 'views/ui_media_object.html'
        })
        .state('app.ui.buttons', {
            url: '/buttons',
            data: { pageTitle: 'UI Buttons' },
            templateUrl: 'views/ui_buttons.html'
        })
        .state('app.ui.icons', {
            url: '/font-awesome',
            data: { pageTitle: 'UI FontAwesome' },
            templateUrl: 'views/ui_icons.html'
        })
        .state('app.ui.simpleLineIcons', {
            url: '/simple-line-icons',
            data: { pageTitle: 'UI Simple Line Icons' },
            templateUrl: 'views/ui_simple_line_icons.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        files: [
                            '/static/dashboard_assets/plugins/simple-line-icons/css/simple-line-icons.css'
                        ]
                    });
                }]
            }
        })
        .state('app.ui.ionicons', {
            url: '/ionicons',
            data: { pageTitle: 'UI Ionicons' },
            templateUrl: 'views/ui_ionicons.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        files: [
                            '/static/dashboard_assets/plugins/ionicons/css/ionicons.min.css'
                        ]
                    });
                }]
            }
        })
        .state('app.ui.tree', {
            url: '/tree',
            data: { pageTitle: 'UI Tree View' },
            templateUrl: 'views/ui_tree.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        files: [
                            '/static/dashboard_assets/plugins/jstree/dist/themes/default/style.min.css',
                            '/static/dashboard_assets/plugins/jstree/dist/jstree.min.js'
                        ]
                    });
                }]
            }
        })
        .state('app.ui.languageBarIcon', {
            url: '/language-bar-icon',
            data: { pageTitle: 'UI Language Bar Icon' },
            templateUrl: 'views/ui_language_bar_icon.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        files: [
                            '/static/dashboard_assets/plugins/flag-icon/css/flag-icon.css'
                        ]
                    });
                }]
            }
        })
        .state('app.ui.socialButtons', {
            url: '/social-buttons',
            data: { pageTitle: 'UI Social Buttons' },
            templateUrl: 'views/ui_social_buttons.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        files: [
                            '/static/dashboard_assets/plugins/bootstrap-social/bootstrap-social.css'
                        ]
                    });
                }]
            }
        })
        .state('app.ui.tour', {
            url: '/tour',
            data: { pageTitle: 'Intro JS' },
            templateUrl: 'views/ui_tour.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        files: [
                            '/static/dashboard_assets/plugins/intro-js/introjs.css',
                            '/static/dashboard_assets/plugins/intro-js/intro.js'
                        ]
                    });
                }]
            }
        })
        .state('app.bootstrap4', {
            url: '/bootstrap4',
            data: { pageTitle: 'Bootstrap 4' },
            templateUrl: 'views/bootstrap_4.html'
        })
        .state('app.form', {
            url: '/form',
            template: '<div ui-view></div>',
            abstract: true
        })
        .state('app.form.elements', {
            url: '/elements',
            data: { pageTitle: 'Form Elements' },
            templateUrl: 'views/form_elements.html'
        })
        .state('app.form.plugins', {
            url: '/plugins',
            data: { pageTitle: 'Form Plugins' },
            templateUrl: 'views/form_plugins.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/bootstrap-datepicker/css/bootstrap-datepicker.css',
                            '/static/dashboard_assets/plugins/bootstrap-datepicker/css/bootstrap-datepicker3.css',
                            '/static/dashboard_assets/plugins/ionRangeSlider/css/ion.rangeSlider.css',
                            '/static/dashboard_assets/plugins/ionRangeSlider/css/ion.rangeSlider.skinNice.css',
                            '/static/dashboard_assets/plugins/bootstrap-colorpicker/css/bootstrap-colorpicker.min.css',
                            '/static/dashboard_assets/plugins/bootstrap-timepicker/css/bootstrap-timepicker.min.css',
                            '/static/dashboard_assets/plugins/password-indicator/css/password-indicator.css',
                            '/static/dashboard_assets/plugins/bootstrap-combobox/css/bootstrap-combobox.css',
                            '/static/dashboard_assets/plugins/bootstrap-select/bootstrap-select.min.css',
                            '/static/dashboard_assets/plugins/bootstrap-tagsinput/bootstrap-tagsinput.css',
                            '/static/dashboard_assets/plugins/jquery-tag-it/css/jquery.tagit.css',
                            '/static/dashboard_assets/plugins/bootstrap-daterangepicker/daterangepicker.css',
                            '/static/dashboard_assets/plugins/select2/dist/css/select2.min.css',
                            '/static/dashboard_assets/plugins/bootstrap-eonasdan-datetimepicker/build/css/bootstrap-datetimepicker.min.css',
                            '/static/dashboard_assets/plugins/bootstrap-colorpalette/css/bootstrap-colorpalette.css',
                            '/static/dashboard_assets/plugins/jquery-simplecolorpicker/jquery.simplecolorpicker.css',
                            '/static/dashboard_assets/plugins/jquery-simplecolorpicker/jquery.simplecolorpicker-fontawesome.css',
                            '/static/dashboard_assets/plugins/jquery-simplecolorpicker/jquery.simplecolorpicker-glyphicons.css',
                            '/static/dashboard_assets/plugins/bootstrap-datepicker/js/bootstrap-datepicker.js',
                            '/static/dashboard_assets/plugins/ionRangeSlider/js/ion-rangeSlider/ion.rangeSlider.min.js',
                            '/static/dashboard_assets/plugins/bootstrap-colorpicker/js/bootstrap-colorpicker.min.js',
                            '/static/dashboard_assets/plugins/masked-input/masked-input.min.js',
                            '/static/dashboard_assets/plugins/bootstrap-timepicker/js/bootstrap-timepicker.min.js',
                            '/static/dashboard_assets/plugins/password-indicator/js/password-indicator.js',
                            '/static/dashboard_assets/plugins/bootstrap-combobox/js/bootstrap-combobox.js',
                            '/static/dashboard_assets/plugins/bootstrap-select/bootstrap-select.min.js',
                            '/static/dashboard_assets/plugins/bootstrap-tagsinput/bootstrap-tagsinput.min.js',
                            '/static/dashboard_assets/plugins/bootstrap-tagsinput/bootstrap-tagsinput-typeahead.js',
                            '/static/dashboard_assets/plugins/jquery-tag-it/js/tag-it.min.js',
                            '/static/dashboard_assets/plugins/bootstrap-daterangepicker/moment.js',
                            '/static/dashboard_assets/plugins/bootstrap-daterangepicker/daterangepicker.js',
                            '/static/dashboard_assets/plugins/select2/dist/js/select2.min.js',
                            '/static/dashboard_assets/plugins/bootstrap-eonasdan-datetimepicker/build/js/bootstrap-datetimepicker.min.js',
                            '/static/dashboard_assets/plugins/bootstrap-show-password/bootstrap-show-password.js',
                            '/static/dashboard_assets/plugins/bootstrap-colorpalette/js/bootstrap-colorpalette.js',
                            '/static/dashboard_assets/plugins/jquery-simplecolorpicker/jquery.simplecolorpicker.js',
                            '/static/dashboard_assets/plugins/clipboard/clipboard.min.js'
                        ]
                    });
                }]
            }
        })
        .state('app.form.sliderSwitcher', {
            url: '/slider-switcher',
            data: { pageTitle: 'Form Slider + Switcher' },
            templateUrl: 'views/form_slider_switcher.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        files: [
                            '/static/dashboard_assets/plugins/switchery/switchery.min.css',
                            '/static/dashboard_assets/plugins/powerange/powerange.min.css',
                            '/static/dashboard_assets/plugins/switchery/switchery.min.js',
                            '/static/dashboard_assets/plugins/powerange/powerange.min.js'
                        ]
                    });
                }]
            }
        })
        .state('app.form.summernote', {
            url: '/summernote',
            data: { pageTitle: 'Summernote' },
            templateUrl: 'views/form_summernote.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        files: [
                            '/static/dashboard_assets/plugins/summernote/summernote.css',
	                        '/static/dashboard_assets/plugins/summernote/summernote.min.js'
                        ]
                    });
                }]
            }
        })
        .state('app.form.dropzone', {
            url: '/dropzone',
            data: { pageTitle: 'Dropzone' },
            templateUrl: 'views/form_dropzone.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        files: [
                            '/static/dashboard_assets/plugins/dropzone/min/dropzone.min.css',
                            '/static/dashboard_assets/plugins/dropzone/min/dropzone.min.js'
                        ]
                    });
                }]
            }
        })
        .state('app.form.validation', {
            url: '/validation',
            data: { pageTitle: 'Form Validation' },
            templateUrl: 'views/form_validation.html'
        })
        .state('app.table', {
            url: '/table',
            template: '<div ui-view></div>',
            abstract: true
        })
        .state('app.table.basic', {
            url: '/basic',
            data: { pageTitle: 'Basic Table' },
            templateUrl: 'views/table_basic.html'
        })
        .state('app.table.manage', {
            url: '/manage',
            template: '<div ui-view></div>',
            abstract: true
        })
        .state('app.table.manage.default', {
            url: '/default',
            data: { pageTitle: 'Managed Table Default' },
            templateUrl: 'views/table_manage.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/DataTables/media/css/dataTables.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/css/responsive.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/media/js/jquery.dataTables.js',
                            '/static/dashboard_assets/plugins/DataTables/media/js/dataTables.bootstrap.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/js/dataTables.responsive.min.js'
                        ]
                    });
                }]
            }
        })
        .state('app.table.manage.autofill', {
            url: '/autofill',
            data: { pageTitle: 'Managed Table Autofill' },
            templateUrl: 'views/table_manage_autofill.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/DataTables/media/css/dataTables.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/AutoFill/css/autoFill.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/css/responsive.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/media/js/jquery.dataTables.js',
                            '/static/dashboard_assets/plugins/DataTables/media/js/dataTables.bootstrap.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/AutoFill/js/dataTables.autoFill.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/AutoFill/js/autoFill.bootstrap.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/js/dataTables.responsive.min.js'
                        ]
                    });
                }]
            }

        })
        .state('app.table.manage.buttons', {
            url: '/buttons',
            data: { pageTitle: 'Managed Table Buttons' },
            templateUrl: 'views/table_manage_buttons.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/DataTables/media/css/dataTables.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Buttons/css/buttons.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/css/responsive.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/media/js/jquery.dataTables.js',
                            '/static/dashboard_assets/plugins/DataTables/media/js/dataTables.bootstrap.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Buttons/js/dataTables.buttons.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Buttons/js/buttons.bootstrap.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Buttons/js/buttons.flash.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Buttons/js/jszip.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Buttons/js/pdfmake.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Buttons/js/vfs_fonts.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Buttons/js/buttons.html5.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Buttons/js/buttons.print.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/js/dataTables.responsive.min.js'
                        ]
                    });
                }]
            }
        })
        .state('app.table.manage.colReorder', {
            url: '/colreorder',
            data: { pageTitle: 'Managed Table ColReorder' },
            templateUrl: 'views/table_manage_colreorder.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/DataTables/media/css/dataTables.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/ColReorder/css/colReorder.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/css/responsive.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/media/js/jquery.dataTables.js',
                            '/static/dashboard_assets/plugins/DataTables/media/js/dataTables.bootstrap.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/ColReorder/js/dataTables.colReorder.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/js/dataTables.responsive.min.js'
                        ]
                    });
                }]
            }
        })
        .state('app.table.manage.fixedColumns', {
            url: '/fixed-column',
            data: { pageTitle: 'Managed Table Fixed Columns' },
            templateUrl: 'views/table_manage_fixed_columns.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/DataTables/media/css/dataTables.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/FixedColumns/css/fixedColumns.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/media/js/jquery.dataTables.js',
                            '/static/dashboard_assets/plugins/DataTables/media/js/dataTables.bootstrap.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/FixedColumns/js/dataTables.fixedColumns.min.js'
                        ]
                    });
                }]
            }
        })
        .state('app.table.manage.fixedHeader', {
            url: '/fixed-header',
            data: { pageTitle: 'Managed Table Fixed Header' },
            templateUrl: 'views/table_manage_fixed_header.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/DataTables/media/css/dataTables.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/FixedHeader/css/fixedHeader.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/css/responsive.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/media/js/jquery.dataTables.js',
                            '/static/dashboard_assets/plugins/DataTables/media/js/dataTables.bootstrap.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/FixedHeader/js/dataTables.fixedHeader.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/js/dataTables.responsive.min.js'
                        ]
                    });
                }]
            }
        })
        .state('app.table.manage.keyTable', {
            url: '/keytable',
            data: { pageTitle: 'Managed Table KeyTable' },
            templateUrl: 'views/table_manage_keytable.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/DataTables/media/css/dataTables.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/KeyTable/css/keyTable.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/css/responsive.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/media/js/jquery.dataTables.js',
                            '/static/dashboard_assets/plugins/DataTables/media/js/dataTables.bootstrap.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/KeyTable/js/dataTables.keyTable.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/js/dataTables.responsive.min.js'
                        ]
                    });
                }]
            }
        })
        .state('app.table.manage.responsive', {
            url: '/responsive',
            data: { pageTitle: 'Managed Table Responsive' },
            templateUrl: 'views/table_manage_responsive.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/DataTables/media/css/dataTables.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/css/responsive.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/media/js/jquery.dataTables.js',
                            '/static/dashboard_assets/plugins/DataTables/media/js/dataTables.bootstrap.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/js/dataTables.responsive.min.js'
                        ]
                    });
                }]
            }
        })
        .state('app.table.manage.rowReorder', {
            url: '/rowreorder',
            data: { pageTitle: 'Managed Table RowReorder' },
            templateUrl: 'views/table_manage_rowreorder.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/DataTables/media/css/dataTables.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/RowReorder/css/rowReorder.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/css/responsive.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/media/js/jquery.dataTables.js',
                            '/static/dashboard_assets/plugins/DataTables/media/js/dataTables.bootstrap.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/RowReorder/js/dataTables.rowReorder.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/js/dataTables.responsive.min.js'
                        ]
                    });
                }]
            }
        })
        .state('app.table.manage.scroller', {
            url: '/scroller',
            data: { pageTitle: 'Managed Table Scroller' },
            templateUrl: 'views/table_manage_scroller.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/DataTables/media/css/dataTables.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Scroller/css/scroller.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/css/responsive.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/media/js/jquery.dataTables.js',
                            '/static/dashboard_assets/plugins/DataTables/media/js/dataTables.bootstrap.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Scroller/js/dataTables.scroller.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/js/dataTables.responsive.min.js'
                        ]
                    });
                }]
            }
        })
        .state('app.table.manage.select', {
            url: '/select',
            data: { pageTitle: 'Managed Table Select' },
            templateUrl: 'views/table_manage_select.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/DataTables/media/css/dataTables.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Select/css/select.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/css/responsive.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/media/js/jquery.dataTables.js',
                            '/static/dashboard_assets/plugins/DataTables/media/js/dataTables.bootstrap.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Select/js/dataTables.select.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/js/dataTables.responsive.min.js'
                        ]
                    });
                }]
            }
        })
        .state('app.table.manage.combine', {
            url: '/combine',
            data: { pageTitle: 'Managed Table Extension Combination' },
            templateUrl: 'views/table_manage_combine.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/DataTables/media/css/dataTables.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Buttons/css/buttons.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/css/responsive.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/AutoFill/css/autoFill.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/ColReorder/css/colReorder.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/KeyTable/css/keyTable.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/RowReorder/css/rowReorder.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Select/css/select.bootstrap.min.css',
                            '/static/dashboard_assets/plugins/DataTables/media/js/jquery.dataTables.js',
                            '/static/dashboard_assets/plugins/DataTables/media/js/dataTables.bootstrap.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Buttons/js/dataTables.buttons.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Buttons/js/buttons.bootstrap.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Buttons/js/buttons.flash.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Buttons/js/jszip.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Buttons/js/pdfmake.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Buttons/js/vfs_fonts.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Buttons/js/buttons.html5.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Buttons/js/buttons.print.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Responsive/js/dataTables.responsive.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/AutoFill/js/dataTables.autoFill.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/ColReorder/js/dataTables.colReorder.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/KeyTable/js/dataTables.keyTable.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/RowReorder/js/dataTables.rowReorder.min.js',
                            '/static/dashboard_assets/plugins/DataTables/extensions/Select/js/dataTables.select.min.js'
                        ]
                    });
                }]
            }
        })
        .state('app.chart', {
            url: '/chart',
            template: '<div ui-view></div>',
            abstract: true
        })
        .state('app.chart.flot', {
            url: '/flot',
            data: { pageTitle: 'Flot Chart' },
            templateUrl: 'views/chart_flot.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        name: 'angular-flot',
                        files: [
                            '/static/dashboard_assets/plugins/flot/jquery.flot.min.js',
                            '/static/dashboard_assets/plugins/flot/jquery.flot.time.min.js',
                            '/static/dashboard_assets/plugins/flot/jquery.flot.resize.min.js',
                            '/static/dashboard_assets/plugins/flot/jquery.flot.pie.min.js',
                            '/static/dashboard_assets/plugins/flot/jquery.flot.stack.min.js',
                            '/static/dashboard_assets/plugins/flot/jquery.flot.crosshair.min.js',
                            '/static/dashboard_assets/plugins/flot/jquery.flot.categories.js',
                            '/static/dashboard_assets/plugins/flot/angular-flot.js',
                        ]
                    })
                }]
            }
        })
        .state('app.chart.morris', {
            url: '/morris',
            data: { pageTitle: 'Morris Chart' },
            templateUrl: 'views/chart_morris.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        files: [
                            '/static/dashboard_assets/plugins/morris/morris.css',
                            '/static/dashboard_assets/plugins/morris/raphael.min.js',
                            '/static/dashboard_assets/plugins/morris/morris.js'
                        ]
                    })
                }]
            }
        })
        .state('app.chart.js', {
            url: '/chart-js',
            data: { pageTitle: 'Chart JS' },
            templateUrl: 'views/chart_js.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        name: 'chart.js',
                        files: [
                            '/static/dashboard_assets/plugins/chart-js/Chart.min.js',
                            '/static/dashboard_assets/plugins/chart-js/angular/angular-chart.min.js'
                        ]
                    })
                }]
            }
        })
        .state('app.chart.d3', {
            url: '/chart-d3',
            data: { pageTitle: 'Chart d3' },
            templateUrl: 'views/chart_d3.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/nvd3/build/nv.d3.css',
                            'https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.2/d3.min.js',
                            '/static/dashboard_assets/plugins/nvd3/build/nv.d3.js'
                        ]
                    })
                }]
            }
        })
        .state('app.calendar', {
            url: '/calendar',
            data: { pageTitle: 'Calendar' },
            templateUrl: 'views/calendar.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/fullcalendar/lib/moment.min.js',
                            '/static/dashboard_assets/plugins/fullcalendar/fullcalendar.min.css',
                            '/static/dashboard_assets/plugins/fullcalendar/fullcalendar.min.js'
                        ]
                    })
                }]
            }
        })
        .state('app.map', {
            url: '/map',
            template: '<div ui-view></div>',
            abstract: true
        })
        .state('app.map.vector', {
            url: '/vector',
            data: { pageTitle: 'Vector Map' },
            templateUrl: 'views/map_vector.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap.css',
                            '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap.min.js',
                            '/static/dashboard_assets/plugins/jquery-jvectormap/jquery-jvectormap-world-mill-en.js'
                        ]
                    })
                }]
            }
        })
        .state('app.map.google', {
            url: '/google',
            data: { pageTitle: 'Google Map' },
            templateUrl: 'views/map_google.html'
        })
        .state('app.gallery', {
            url: '/gallery',
            template: '<div ui-view></div>',
            abstract: true
        })
        .state('app.gallery.v1', {
            url: '/v1',
            data: { pageTitle: 'Gallery V1' },
            templateUrl: 'views/gallery.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/isotope/isotope.css',
                            '/static/dashboard_assets/plugins/lightbox/css/lightbox.css',
                            '/static/dashboard_assets/plugins/isotope/jquery.isotope.min.js',
                            '/static/dashboard_assets/plugins/lightbox/js/lightbox.min.js'
                        ]
                    })
                }]
            }
        })
        .state('app.gallery.v2', {
            url: '/v2',
            data: { pageTitle: 'Gallery V2' },
            templateUrl: 'views/gallery_v2.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        serie: true,
                        files: [
                            '/static/dashboard_assets/plugins/superbox/js/superbox.js'
                        ]
                    })
                }]
            }
        })
        .state('app.options', {
            url: '/options',
            template: '<div ui-view></div>',
            abstract: true
        })
        .state('app.options.pageBlank', {
            url: '/blank',
            data: { pageTitle: 'Blank Page' },
            templateUrl: 'views/page_blank.html'
        })
        .state('app.options.pageWithFooter', {
            url: '/with-footer',
            data: { pageTitle: 'Page with Footer' },
            templateUrl: 'views/page_with_footer.html'
        })
        .state('app.options.pageWithoutSidebar', {
            url: '/without-sidebar',
            data: { pageTitle: 'Page without Sidebar' },
            templateUrl: 'views/page_without_sidebar.html'
        })
        .state('app.options.pageWithRightSidebar', {
            url: '/right-sidebar',
            data: { pageTitle: 'Page with Right Sidebar' },
            templateUrl: 'views/page_with_right_sidebar.html'
        })
        .state('app.options.pageWithMinifiedSidebar', {
            url: '/minified-sidebar',
            data: { pageTitle: 'Page with Minified Sidebar' },
            templateUrl: 'views/page_with_minified_sidebar.html'
        })
        .state('app.options.pageWithTwoSidebar', {
            url: '/two-sidebar',
            data: { pageTitle: 'Page with Two Sidebar' },
            templateUrl: 'views/page_with_two_sidebar.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        files: [
                            '/static/dashboard_assets/plugins/sparkline/jquery.sparkline.js',
                            '/static/dashboard_assets/plugins/jquery-knob/js/jquery.knob.js'
                        ]
                    })
                }]
            }
        })
        .state('app.options.pageFullHeightContent', {
            url: '/full-height-content',
            data: { pageTitle: 'Full Height Content' },
            templateUrl: 'views/page_full_height.html'
        })
        .state('app.options.pageWithWideSidebar', {
            url: '/wide-sidebar',
            data: { pageTitle: 'Page with Wide Sidebar' },
            templateUrl: 'views/page_with_wide_sidebar.html'
        })
        .state('app.options.pageWithLightSidebar', {
            url: '/light-sidebar',
            data: { pageTitle: 'Page with Light Sidebar' },
            templateUrl: 'views/page_with_light_sidebar.html'
        })
        .state('app.options.pageWithMegaMenu', {
            url: '/light-sidebar',
            data: { pageTitle: 'Page with Mega Menu' },
            templateUrl: 'views/page_with_mega_menu.html'
        })
        .state('app.options.pageWithTopMenu', {
            url: '/top-menu',
            data: { pageTitle: 'Page with Top Menu' },
            templateUrl: 'views/page_with_top_menu.html'
        })
        .state('app.options.pageWithMixedMenu', {
            url: '/mixed-menu',
            data: { pageTitle: 'Page with Mixed Menu' },
            templateUrl: 'views/page_with_mixed_menu.html'
        })
        .state('app.options.pageWithBoxedLayout', {
            url: '/boxed-layout',
            data: { pageTitle: 'Page with Boxed Layout' },
            templateUrl: 'views/page_with_boxed_layout.html'
        })
        .state('app.options.pageWithBoxedMixedMenu', {
            url: '/boxed-mixed-menu',
            data: { pageTitle: 'Page with Mixed Menu Boxed Layout' },
            templateUrl: 'views/page_boxed_layout_with_mixed_menu.html'
        })
        .state('app.options.pageWithTransparentSidebar', {
            url: '/transparent-sidebar',
            data: { pageTitle: 'Page with Transparent Sidebar' },
            templateUrl: 'views/page_with_transparent_sidebar.html'
        })
        */
        .state('app.extra', {
            url: '/extra',
            template: '<div ui-view></div>',
            abstract: true
        })
        .state('app.extra.timeline', {
            url: '/timeline',
            data: { pageTitle: 'Timeline' },
            templateUrl: 'views/extra_timeline.html'
        })
        .state('app.extra.searchResults', {
            url: '/search-results',
            data: { pageTitle: 'Search Results' },
            templateUrl: 'views/extra_search_results.html'
        })
        .state('app.extra.invoice', {
            url: '/invoice',
            data: { pageTitle: 'Invoice' },
            templateUrl: 'views/extra_invoice.html'
        })
        .state('app.extra.profile', {
            url: '/profile',
            data: { pageTitle: 'Profile' },
            templateUrl: 'views/extra_profile.html'
        })
        .state('comingSoon', {
            url: '/coming-soon',
            data: { pageTitle: 'Coming Soon' },
            templateUrl: 'views/extra_coming_soon.html',
            resolve: {
                service: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        files: [
                            '/static/dashboard_assets/plugins/jquery.countdown/jquery.countdown.css',
                            '/static/dashboard_assets/plugins/jquery.countdown/jquery.plugin.js',
                            '/static/dashboard_assets/plugins/jquery.countdown/jquery.countdown.js'
                        ]
                    })
                }]
            }
        })
        .state('error', {
            url: '/error',
            data: { pageTitle: '404 Error' },
            templateUrl: 'views/extra_404_error.html'
        })
        .state('member', {
            url: '/member',
            template: '<div ui-view></div>',
            abstract: true
        })
        .state('member.login', {
            url: '/login',
            template: '<div ui-view></div>',
            abstract: true
        })
        .state('member.login.v1', {
            url: '/v1',
            data: { pageTitle: 'Login' },
            templateUrl: 'views/login.html'
        })
        .state('member.login.v2', {
            url: '/v2',
            data: { pageTitle: 'Login V2' },
            templateUrl: 'views/login_v2.html'
        })
        .state('member.login.v3', {
            url: '/v3',
            data: { pageTitle: 'Login V3' },
            templateUrl: 'views/login_v3.html'
        })
        .state('member.register', {
            url: '/register',
            data: { pageTitle: 'Register V3' },
            templateUrl: 'views/register_v3.html'
        })
        .state('app.helper', {
            url: '/helper',
            template: '<div ui-view></div>',
            abstract: true
        })
        .state('app.helper.css', {
            url: '/css',
            data: { pageTitle: 'Predefined CSS Classes' },
            templateUrl: 'views/helper_css.html'
        })
}]);

colorAdminApp.run(['$rootScope', '$state', 'setting', function($rootScope, $state, setting) {
    $rootScope.$state = $state;
    $rootScope.setting = setting;
}]);
