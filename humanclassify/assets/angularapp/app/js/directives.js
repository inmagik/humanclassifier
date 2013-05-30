'use strict';

/* Directives */

/*todo: move away or find sth else */
function listToMatrix(list, elementsPerSubArray) {
    var matrix = [], i, k;

    for (i = 0, k = -1; i < list.length; i++) {
        if (i % elementsPerSubArray === 0) {
            k++;
            matrix[k] = [];
        }

        matrix[k].push(list[i]);
    }

    return matrix;
}



var directives = angular.module('myApp.directives', []);
directives.directive('appVersion', ['version', function(version) {
  return function(scope, elm, attrs) {
    elm.text(version);
  };
}]);



directives.directive('fillingButtons', [function() {
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


directives.directive('refPlantTable', [function() {
  return {
            restrict: 'E',
            template : '<table class="table"></table>',
            /*scope : {
                refPlant : '='
            },
            */
            link: function(scope, element, attrs){
                
                var tableFields = attrs.tableFields;
                if(!tableFields) return;

                 
                
                var fieldsPerRow = parseInt(attrs.fieldsPerRow) || 1;
                var fields = tableFields.split(",");
            
                
                var matrix = listToMatrix(fields, fieldsPerRow);
                
                
                var update = function(sourceObj){
                    for(var i=0, n=matrix.length; i<n; i++){
                        var row = matrix[i];
                        var tRow = $('<tr></tr>');
                        
                        for(var j=0, m=row.length; j<m; j++){
                            var fieldName = row[j];
                            console.log("fn", fieldName);
                            var tColLabel = $('<td></td>').text(fieldName);
                            var tColContent = $('<td></td>').text(sourceObj.fieldName);
                            tRow.append(tColLabel).append(tColContent);
                        }
                        $("table", element).append(tRow);
                    }
                }
                
                scope.$watch('refPlant', function(newValue){
                    console.log("xxx", newValue);
                    update(newValue);
                
                })
                
                
                
               
            }
            
            
            
        };
}]);
