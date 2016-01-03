'use strict';

angular.module('tutorialApp', ['ngAnimate', 'ngRoute'])
  .config(function($routeProvider) {
    $routeProvider

      .when('/', { templateUrl: 'static/main.html' })
      .when('/chart', { templateUrl: 'static/chart.html' })
      
      .otherwise({ redirectTo: '/'});
  })
  .directive('price', function(){
    return {
      restrict: 'E',
      scope: {
        value: '='
      },
      template: '<span ng-show="value == 0">kostenlos</span>' +
        '<span ng-show="value > 0">{{value | currency}}</span>'
    }
  })
  .factory('Cart', function() {

    var text = "";

    return {

    };
  })
  .controller('ArticlesCtrl', function($scope, $http, Cart){
    $scope.cart = Cart;

  })
  .controller('CartCtrl', function($scope, Cart){
    $scope.cart = Cart;
  });
