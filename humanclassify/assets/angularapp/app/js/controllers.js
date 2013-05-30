'use strict';

/* Controllers */

var controllersModule = angular.module('myApp.controllers', []);

controllersModule
  .controller('HomeCtrl', [ function() {

  }])
  
  .controller('PlantsCtrl', ['$scope', function($scope) {

    $scope.plants = "aaaaa";

  }])
  
  .controller('RefPlantsCtrl', ['$scope', 'refPlantsService', function($scope, refPlantsService) {

    $scope.refPlants = [];
    $scope.nextPage = null;
    $scope.radioModel = 'Thumbs';
    
    /* goes through the paginated rest api */
    var getRefPlants = function(allPages){
        var allPages = !!allPages;
        
        var url = $scope.refPlants.length == 0 ? '/api/reference-plants/' 
                    : $scope.nextPage ? $scope.nextPage : null;
        
        refPlantsService.refPlantsList(url).then(function(data){
            
            //temporarily disabled pagination
            $scope.refPlants = data;
            return;
            
            console.log(data);
            $scope.nextPage = data.next;
            $scope.refPlants.push.apply($scope.refPlants, data.results);
            
            if(allPages && data.next) getRefPlants();
            return;
        
        });
    };
    
    getRefPlants(true);
    

  }])
  
  
  .controller('RefPlantCtrl', ['$scope', '$route', 'refPlantsService', function($scope, $route, refPlantsService) {

    $scope.refPlant = {};
    
    var getPlant = function(){
        var id = $route.current.params.refPlantId;
        refPlantsService.refPlant('/api/reference-plants/', id).then(function(data){
            angular.extend($scope.refPlant, data);
        });
        
    }
    getPlant();
    

  }])
  
  .controller('ButtonsCtrl', ['$scope', '$route', function($scope, $route) {
  
    $scope.radioModel = 'Home';

  }]);