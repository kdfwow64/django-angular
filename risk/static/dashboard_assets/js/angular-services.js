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

    var farms = {
        getAllMyRiskTypes: get_all_my_risk_types,
    }
    return farms;
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

    var farms = {
        getAllResponseTypes: get_all_response_types,
    }
    return farms;
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

    var farms = {
        getCompanyLocations: get_all_company_locations,
    }
    return farms;
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

    var farms = {
        getCompliances: get_all_compliances,
    }
    return farms;
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

    var farms = {
        getUsers: get_all_users,
    }
    return farms;
}

colorAdminApp.factory('RiskTypeService', ['$http', RiskTypeService])
             .factory('ResponseTypeService', ['$http', ResponseTypeService])
             .factory('CompanyLocationService', ['$http', CompanyLocationService])
             .factory('ComplianceService', ['$http', ComplianceService])
             .factory('UserService', ['$http', UserService])

