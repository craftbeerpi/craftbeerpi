angular.module('myApp.controllers5', []).controller('VesselOverviewController', function($scope, $location, CBPSteps,CBPVessel) {

  CBPVessel.query({}, function(response) {
    $scope.vessels = response.objects
  });

  $scope.thermometer = [];
  $scope.thermometer.push({"key":"", "value":""});

  CBPVessel.getthermometer({}, function(response) {
    angular.forEach(response, function(d) {
        $scope.thermometer.push({"key":d, "value":d});
    })
  });

  $scope.vessel = {
    "name": "",
    "sensorid": "",
    "heater": "23",
    "agitator": "24",
  }

  $scope.gpio = []
  $scope.gpio.push({
    "key": undefined,
    "value": "NO GPIO",
  });
  for(i = 1; i < 25; i++) {
    $scope.gpio.push({
      "key": i,
      "value": i
    });
  }

  $scope.save = function() {
    console.log( $scope.vessel.name.length)
    if($scope.vessel.name.length == 0) {
      return;
    }
    CBPVessel.save($scope.vessel, function(data) {
      CBPVessel.query({}, function(response) {
        $scope.vessels = response.objects;
      });
    });
  }

}).controller('VesselEditController', function($scope, CBPVessel, $routeParams) {
  // Do something with myService
  $scope.vid = $routeParams.vid

    CBPVessel.get({
      "id": $scope.vid
    }, function(response) {
      $scope.vessel = response;
    });

    $scope.thermometer = [];
    $scope.thermometer.push({"key":"", "value":"No Thermometer"});

    CBPVessel.getthermometer({}, function(response) {

      angular.forEach(response, function(d) {
          $scope.thermometer.push({"key":d, "value":d});
      })
    });

    $scope.gpio = []
    $scope.gpio.push({
      "key": undefined,
      "value": "NO GPIO",
    });
    for(i = 1; i < 25; i++) {
      $scope.gpio.push({
        "key": i,
        "value": i
      });
    }

    $scope.save = function() {

      CBPVessel.update({
        "id": $scope.vessel.id
      }, $scope.vessel, function() {
        history.back();
      });
    }
    $scope.delete = function() {
      CBPVessel.delete({
        "id": $scope.vessel.id
      }, function() {
        history.back();
      });
    }

});
