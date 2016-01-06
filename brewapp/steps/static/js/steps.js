angular.module("myApp").config(function($routeProvider) {
  console.log("HALLO")
  $routeProvider
  .when('/woohoo', {
    templateUrl: '/steps/static/edit_step.html',
    name: "WOOOHOO"
  })

});
