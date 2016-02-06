angular.module('craftberpi.hardware', []).controller('PumpOverviewController', function($scope, $location, CBPPump, ConfirmMessage, CBPKettle, CBPConfig) {


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

  CBPPump.query(function(response) {
    $scope.pumps = response.objects;
  });
  $scope.save = function() {

    if ($scope.pump.name.length == 0) {
      return;
    }
    CBPPump.save($scope.pump, function(data) {
      CBPPump.query(function(response) {
        $scope.pumps = response.objects;
      });
    });

  }

}).controller('PumpEditController', function($scope, $location, $routeParams, CBPPump, ConfirmMessage, CBPKettle, CBPConfig) {

  $scope.vid = $routeParams.vid

  CBPPump.get({
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
    CBPPump.update({
      "id": $scope.pump.id
    }, $scope.pump, function() {
      history.back();
    });
  }
  $scope.delete = function() {
    CBPPump.delete({
      "id": $scope.pump.id
    }, function() {
      history.back();
    });
  }

});
