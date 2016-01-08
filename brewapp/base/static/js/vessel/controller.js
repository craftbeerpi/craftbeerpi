angular.module('myApp.controllers5', []).controller('KettleOverviewController', function($scope, $location, CBPSteps,CBPKettle) {

  CBPKettle.query({}, function(response) {
    $scope.kettles = response.objects
  });

  $scope.thermometer = [];
  $scope.thermometer.push({"key":"", "value":""});

  CBPKettle.getthermometer({}, function(response) {
    angular.forEach(response, function(d) {
        $scope.thermometer.push({"key":d, "value":d});
    })
  });

  $scope.kettle = {
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
    console.log( $scope.kettle.name.length)
    if($scope.kettle.name.length == 0) {
      return;
    }
    CBPKettle.save($scope.kettle, function(data) {
      CBPKettle.query({}, function(response) {
        $scope.kettles = response.objects;
      });
    });
  }

}).controller('KettleEditController', function($scope, CBPKettle, $routeParams) {
  // Do something with myService
  $scope.vid = $routeParams.vid

    CBPKettle.get({
      "id": $scope.vid
    }, function(response) {
      $scope.kettle = response;
    });

    $scope.thermometer = [];
    $scope.thermometer.push({"key":"", "value":"No Thermometer"});

    CBPKettle.getthermometer({}, function(response) {

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

      CBPKettle.update({
        "id": $scope.kettle.id
      }, $scope.kettle, function() {
        history.back();
      });
    }
    $scope.delete = function() {
      CBPKettle.delete({
        "id": $scope.kettle.id
      }, function() {
        history.back();
      });
    }

});
