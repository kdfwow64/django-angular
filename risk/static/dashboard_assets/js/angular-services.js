/**
Atemon Technology Consultants LLP
Version: 0.0.0
Author: Varghese Chacko
Website: http://www.atemon.com/
    ----------------------------
        APPS SERVICES TABLE
    ----------------------------
    1.0 SERVICE - RiskTypeService
    2.0 SERVICE - ResponseTypeService
    3.0 SERVICE - CompanyLocationService
    4.0 SERVICE - ComplianceService
    5.0 SERVICE - UserService
    6.0 SERVICE - ActorService
    7.0 SERVICE - ActorIntentService
    8.0 SERVICE - ActorMotiveService
    9.0 SERVICE - CompanyAssetsService
   10.0 SERVICE - CompanyControlsService
   11.0 SERVICE - CompanyControlMeasuresService
   12.0 SERVICE - WizardValidatorService
   13.0 SERVICE - EntryCompanyControlsService
   14.0 SERVICE - RiskEntryService
   15.0 SERVICE - ImpactTypeService
   16.0 SERVICE - WizardFormService

*/

/* -------------------------------
   1.0 SERVICE - RiskTypeService
------------------------------- */

function RiskTypeService($http){
    function get_all_my_risk_types(){
        return $http.get('/dashboard/api/risk-types/').then(function(r){
            return r.data;
        }, function(r){});
    }

    var service = {
        getAllMyRiskTypes: get_all_my_risk_types,
    }
    return service;
}

/* -----------------------------------
   2.0 SERVICE - ResponseTypeService
--------------------------------------*/

function ResponseTypeService($http){
    function get_all_response_types(){
        return $http.get('/dashboard/api/response-types/').then(function(r){
            return r.data;
        }, function(r){});
    }

    var service = {
        getAllResponseTypes: get_all_response_types,
    }
    return service;
}
/* -----------------------------------
   3.0 SERVICE - CompanyLocationService
--------------------------------------*/

function CompanyLocationService($http){
    function get_all_company_locations(){
        return $http.get('/dashboard/api/company-locations/').then(function(r){
            return r.data;
        }, function(r){});
    }

    var service = {
        getCompanyLocations: get_all_company_locations,
    }
    return service;
}

/* -----------------------------------
   4.0 SERVICE - ComplianceService
--------------------------------------*/

function ComplianceService($http){
    function get_all_compliances(){
        return $http.get('/dashboard/api/compliances/').then(function(r){
            return r.data;
        }, function(r){});
    }

    var service = {
        getCompliances: get_all_compliances,
    }
    return service;
}

/* -----------------------------------
   5.0 SERVICE - UserService
--------------------------------------*/

function UserService($http){
    function get_all_users(){
        return $http.get('/dashboard/api/users/').then(function(r){
            return r.data;
        }, function(r){});
    }

    var service = {
        getUsers: get_all_users,
    }
    return service;
}

/* -----------------------------------
   6.0 SERVICE - ActorService
--------------------------------------*/

function ActorService($http){
    function get_all_actors(){
        return $http.get('/dashboard/api/actors/').then(function(r){
            return r.data;
        }, function(r){});
    }

    var service = {
        getActors: get_all_actors,
    }
    return service;
}

/* -----------------------------------
   7.0 SERVICE - ActorIntentService
--------------------------------------*/

function ActorIntentService($http){
    function get_all_actor_intents(){
        return $http.get('/dashboard/api/actor-intents/').then(function(r){
            return r.data;
        }, function(r){});
    }

    var service = {
        getActorIntents: get_all_actor_intents,
    }
    return service;
}

/* -----------------------------------
   8.0 SERVICE - ActorMotiveService
--------------------------------------*/

function ActorMotiveService($http){
    function get_all_actor_motives(){
        return $http.get('/dashboard/api/actor-motives/').then(function(r){
            return r.data;
        }, function(r){});
    }

    var service = {
        getActorMotives: get_all_actor_motives,
    }
    return service;
}

/* -----------------------------------
   9.0 SERVICE - CompanyAssetsService
--------------------------------------*/

function CompanyAssetsService($http){
    function get_all_company_assets(){
        return $http.get('/dashboard/api/company-assets/').then(function(r){
            return r.data;
        }, function(r){});
    }

    var service = {
        getCompanyAssets: get_all_company_assets,
    }
    return service;
}

/* -----------------------------------
  10.0 SERVICE - CompanyControlsService
--------------------------------------*/

function CompanyControlsService($http){
    function get_all_company_controls(){
        return $http.get('/dashboard/api/company-controls/').then(function(r){
            return r.data;
        }, function(r){});
    }

    var service = {
        getCompanyControls: get_all_company_controls,
    }
    return service;
}

/* -----------------------------------
  11.0 SERVICE - CompanyControlsService
--------------------------------------*/

function CompanyControlsService($http){
    function get_all_company_controls(){
        return $http.get('/dashboard/api/company-controls/').then(function(r){
            return r.data;
        }, function(r){});
    }

    var service = {
        getCompanyControls: get_all_company_controls,
    }
    return service;
}

/* --------------------------------------------
  11.0 SERVICE - CompanyControlMeasuresService
-----------------------------------------------*/

function CompanyControlMeasuresService($http){
    function get_all_company_control_measures(){
        return $http.get('/dashboard/api/company-control-measures/').then(function(r){
            return r.data;
        }, function(r){});
    }

    var service = {
        getCompanyControlMeasures: get_all_company_control_measures,
    }
    return service;
}
/* --------------------------------------------
  12.0 SERVICE - WizardValidatorService
-----------------------------------------------*/

function WizardValidatorService(){
    riskEntryValidator = function (e, ui) {
        $scope = angular.element(e.target).scope()
        if(ui.nextIndex < ui.index){
            switch(ui.index){
                case 1: service.status.basic_info = true; break;
                case 2: service.status.threat_details = true; break;
                case 3: service.status.affected_assets = true; break;
                case 4: service.status.mitigating_controls = true; break;
                case 5: service.status.measurements = true; break;
            }

            return true;
        }
        if (ui.index == 0) {
            // step-1 validation
            if (false === $('form[name="form-wizard"]').parsley().validate('wizard-step-1')) {
                return false;
            }
            else if(service.status.basic_info == false){
                $scope.save_basic_info(this);
                return false;
            }
            else{
                return true;
            }
        } else if (ui.index == 1) {
            // step-2 validation
            if (false === $('form[name="form-wizard"]').parsley().validate('wizard-step-2')) {
                return false;
            }else if(service.status.threat_details == false){
                $scope.save_threat_details(this);
                return false;
            }
            else{
                return true;
            }
        } else if (ui.index == 2) {
            // step-3 validation
            if (false === $('form[name="form-wizard"]').parsley().validate('wizard-step-3')) {
                return false;
            }else if(service.status.affected_assets == false){
                $scope.save_affected_assets(this);
                return false;
            }
            else{
                return true;
            }
        }else if (ui.index == 3) {
            // step-4 validation
            if (false === $('form[name="form-wizard"]').parsley().validate('wizard-step-4')) {
                return false;
            }else if(service.status.mitigating_controls == false){
                $scope.save_mitigating_controls(this);
                return false;
            }
            else{
                return true;
            }
        }else if (ui.index == 4) {
            // step-5 validation
            if (false === $('form[name="form-wizard"]').parsley().validate('wizard-step-5')) {
                return false;
            }else if(service.status.measurements == false){
                $scope.save_measurements(this);
                return false;
            }
            else{
                return true;
            }
        }
    }

    var service = {
        riskEntryValidator: riskEntryValidator,
        status: {
            basic_info: false,
            threat_details: false,
            affected_assets: false,
            mitigating_controls: false,
            measurements:false,
        },
        set: function(){
            this.status= {
                basic_info: false,
                threat_details: true,
                affected_assets: true,
                mitigating_controls: true,
                measurements:true,
            }
        },
        reset: function(){
            this.status= {
                basic_info: false,
                threat_details: false,
                affected_assets: false,
                mitigating_controls: false,
                measurements:false,
            }
        },
    }
    return service;
}

/* -----------------------------------
  13.0 SERVICE - EntryCompanyControlsService
--------------------------------------*/

function EntryCompanyControlsService($http){
    function get_all_entry_company_controls(){
        return $http.get('/dashboard/api/entry-company-controls/').then(function(r){
            return r.data;
        }, function(r){});
    }

    var service = {
        getEntryCompanyControls: get_all_entry_company_controls,
    }
    return service;
}

/* -----------------------------------
  14.0 SERVICE - RiskEntryService
--------------------------------------*/

function RiskEntryService($http){
    function get_selected_risk_entry(id){
        return $http.get('/dashboard/api/risk-entry/' + id + '/').then(function(r){
            return r.data;
        }, function(r){return {}});
        // TODO: Resole properly when id=0, ie adding an entry
    }

    var service = {
        getselectedRiskEntry: get_selected_risk_entry,
    }
    return service;
}

/* -----------------------------------
  15.0 SERVICE - ImpactTypeService
--------------------------------------*/

function ImpactTypeService($http){
    function get_all_impact_types(id){
        return $http.get('/dashboard/api/impact-types/').then(function(r){
            return r.data;
        }, function(r){return {}});
    }

    var service = {
        getAllImpactTypes: get_all_impact_types,
    }
    return service;
}
/* -----------------------------------
  15.6 SERVICE - WizardFormService
--------------------------------------*/

function WizardFormService($http){
    function get_threat_detail_form(){
        return {
            entry_actor_id: null,
            actor_name: null,
            intentions: [],
            motives: [],
            detail: null,
        }

    }
    function get_affected_assets_form(){
        return {
            entry_asset_id: null,
            asset_name: null,
            exposure_percentage: 100,
            detail: null,
            impact_notes: null,
        }

    }

    function get_mitigating_controls_form(){
        return {
            entry_mcontrol_id: null,
            control: null,
            mitigation_rate: 100,
            notes: null,
            url: null,
            addtional_mitigation: null,
        }

    }

    function get_measurements_form(){
        return {
            entry_mcontrol_id: null,
            control: null,
            measurement: [],
        }

    }

    var service = {
        get_threat_detail_form: get_threat_detail_form,
        get_affected_assets_form: get_affected_assets_form,
        get_mitigating_controls_form: get_mitigating_controls_form,
        get_measurements_form: get_measurements_form,
    }
    return service;
}

colorAdminApp.factory('RiskTypeService', ['$http', RiskTypeService])
             .factory('ResponseTypeService', ['$http', ResponseTypeService])
             .factory('CompanyLocationService', ['$http', CompanyLocationService])
             .factory('ComplianceService', ['$http', ComplianceService])
             .factory('UserService', ['$http', UserService])
             .factory('ActorService', ['$http', ActorService])
             .factory('ActorIntentService', ['$http', ActorIntentService])
             .factory('ActorMotiveService', ['$http', ActorMotiveService])
             .factory('CompanyAssetsService', ['$http', CompanyAssetsService])
             .factory('CompanyControlsService', ['$http', CompanyControlsService])
             .factory('EntryCompanyControlsService', ['$http', EntryCompanyControlsService])
             .factory('CompanyControlMeasuresService', ['$http', CompanyControlMeasuresService])
             .factory('WizardValidatorService', [WizardValidatorService])
             .factory('RiskEntryService', ['$http', RiskEntryService])
             .factory('ImpactTypeService', ['$http', ImpactTypeService])
             .factory('WizardFormService', [WizardFormService])