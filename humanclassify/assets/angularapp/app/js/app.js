'use strict';


// Declare app level module which depends on filters, and services
angular.module('myApp', ['myApp.filters', 'myApp.services', 'myApp.directives', 'myApp.controllers']).

  config(['$routeProvider', function($routeProvider) {

    $routeProvider.when('/home', {templateUrl: 'partials/home.html', controller: 'HomeCtrl'});
    $routeProvider.when('/plants', {templateUrl: 'partials/partial2.html', controller: 'PlantsCtrl'});
    $routeProvider.when('/refplants', {templateUrl: 'partials/reference_plants.html', controller: 'RefPlantsCtrl'});
    $routeProvider.otherwise({redirectTo: '/home'});
  
}]);
