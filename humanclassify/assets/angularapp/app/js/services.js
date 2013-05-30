'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('myApp.services', []).
  value('version', '0.1');

angular.module('myApp.services', [])
.factory('refPlantsService', function($http, $q) {
  return {
    
    refPlantsList : function(apiUrl){
        //dumb and static for now, but already using a deferred
        var deferred = $q.defer();
        $http.get(apiUrl).success(function(data){
            deferred.resolve(data);
        }).error(function(){
            deferred.reject("An error occured while fetching spec");
        });
        return deferred.promise;

    },
    
    refPlant : function(apiUrl, plantId){

        var deferred = $q.defer();
        $http.get(apiUrl + plantId).success(function(data){
            deferred.resolve(data);
        }).error(function(){
            deferred.reject("An error occured while fetching spec");
        });
        
        return deferred.promise;
    }
    
    
  }
});