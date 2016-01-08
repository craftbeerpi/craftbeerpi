angular.module('myApp.controllers6', []).controller('SetupController', function(ws, $scope, $http, $uibModal, $location) {

  $scope.setup = function(num) {
    $http.post("/api/kettle/setup/"+num).success(function(data, status, headers, config) {
        $location.url("/kettle/overview");
    });
  }
});
