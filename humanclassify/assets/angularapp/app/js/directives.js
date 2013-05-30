'use strict';

/* Directives */



var directives = angular.module('myApp.directives', []);
directives.directive('appVersion', ['version', function(version) {
  return function(scope, elm, attrs) {
    elm.text(version);
  };
}]);



directives.directive('bottomButtons', [function() {
  return {
            restrict: 'A',
            link: function(scope, element, attrs)
            {
                
                var btnGroup = $(".btn-group", element);
                btnGroup.css('width', '100%');
                var buttons = $("button", element);
                var num = buttons.size();
                var btnWidth = 100.0 / parseFloat(num);
                buttons.css('width', btnWidth+'%');
            }
        };
}]);



directives.directive('pageButton', ['$location', function($location) {
  return {
            restrict: 'A',
            link: function(scope, element, attrs)
            {
            
                var path = attrs.pageButton;
                if(!path){
                    return;
                };
                
                element.on('click', function(){
                    console.log("pp", path);       
                    $location.path(path);
                });
            }
        };
}]);
