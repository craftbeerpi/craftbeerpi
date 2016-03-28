angular.module('craftberpi.hardware', []).controller('PumpOverviewController', function($scope, $location, CBPHardware, ConfirmMessage, CBPKettle, CBPConfig) {


  $scope.pump = {
    "name": "",
    "switch": undefined,
  }

  $scope.gpio = []


  CBPKettle.getDevices({}, function(response) {
    angular.forEach(response, function(d) {
      $scope.gpio.push({
        "key": d,
        "value": d
      });
    })
  });

  CBPHardware.query(function(response) {
    $scope.pumps = response.objects;
  });
  $scope.save = function() {

    if ($scope.pump.name.length == 0) {
      return;
    }
    CBPHardware.save($scope.pump, function(data) {
      CBPHardware.query(function(response) {
        $scope.pumps = response.objects;
      });
    });

  }

}).controller('PumpEditController', function($scope, $location, $routeParams, CBPHardware, ConfirmMessage, CBPKettle, CBPConfig) {

  $scope.vid = $routeParams.vid

  CBPHardware.get({
    "id": $scope.vid
  }, function(response) {
    $scope.pump = response;
  });

  $scope.gpio = []

  CBPKettle.getDevices({}, function(response) {
    angular.forEach(response, function(d) {
      $scope.gpio.push({
        "key": d,
        "value": d
      });
    })
  });

  $scope.save = function() {
    CBPHardware.update({
      "id": $scope.pump.id
    }, $scope.pump, function() {
      history.back();
    });
  }
  $scope.delete = function() {

    ConfirmMessage.open("Delete Hardware","Do you really want to delete the hardware?", function() {
      CBPHardware.delete({
        "id": $scope.pump.id
      }, function() {
        history.back();
      });

    }, function() {

    });




  }

});
