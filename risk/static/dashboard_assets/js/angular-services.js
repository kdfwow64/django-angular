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

*/

/* -------------------------------
   1.0 SERVICE - RiskTypeService
------------------------------- */

function RiskTypeService($http){
    function get_all_my_risk_types($scope){
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
    function get_all_response_types($scope){
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
    function get_all_company_locations($scope){
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
    function get_all_compliances($scope){
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
    function get_all_users($scope){
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
    function get_all_actors($scope){
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
    function get_all_actor_intents($scope){
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
    function get_all_actor_motives($scope){
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
    function get_all_company_assets($scope){
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
    function get_all_company_controls($scope){
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
    function get_all_company_controls($scope){
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
    function get_all_company_control_measures($scope){
        return $http.get('/dashboard/api/company-control-measures/').then(function(r){
            return r.data;
        }, function(r){});
    }

    var service = {
        getCompanyControlMeasures: get_all_company_control_measures,
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
             .factory('CompanyControlMeasuresService', ['$http', CompanyControlMeasuresService])

