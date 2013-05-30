'use strict';

/* Controllers */

angular.module('myApp.controllers', [])
  
  .controller('HomeCtrl', [ function() {

  }])
  
  .controller('PlantsCtrl', ['$scope', function($scope) {

    $scope.plants = "aaaaa";

  }])
  
  .controller('RefPlantsCtrl', ['$scope', 'refPlantsService', function($scope, refPlantsService) {

    $scope.refPlants = [];
    $scope.nextPage = null;
    
    /* goes through the paginated rest api */
    var getRefPlants = function(allPages){
        var allPages = !!allPages;
        
        var url = $scope.refPlants.length == 0 ? '/api/reference-plants/' 
                    : $scope.nextPage ? $scope.nextPage : null;
        
        refPlantsService.refPlantsList(url).then(function(data){
        
            console.log(data);
            $scope.nextPage = data.next;
            $scope.refPlants.push.apply($scope.refPlants, data.results);
            
            if(allPages && data.next) getRefPlants();
            return;
        
        });
    };
    
    getRefPlants(true);
    

  }]);