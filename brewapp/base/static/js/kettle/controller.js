angular.module('craftberpi.controllers5', []).controller('KettleOverviewController', function($scope, $location, CBPSteps,CBPKettle, ConfirmMessage, CBPConfig) {

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

  $scope.automatic = [];
  CBPKettle.getautomatic({}, function(response) {
    $scope.automatic = response;

  });

  $scope.kettle = {
    "name": "",
    "sensorid": "",
    "heater": undefined,
    "agitator": undefined,
  }

  $scope.gpio = []
  $scope.gpio.push({
    "key": undefined,
    "value": "NO GPIO",
  });

  CBPKettle.getDevices({}, function(response) {
    angular.forEach(response, function(d) {
        $scope.gpio.push({"key":d, "value":d});
    })
  });


  $scope.clearTempLogs = function() {
    ConfirmMessage.open("Clear Temperature Log","Do you really want to clear all Temperature Logs?", function() {
      CBPKettle.clear({}, function(response) {

      });
    }, function() {

    });
  }

  $scope.clear = function() {
    $scope.kettle = {
      "name": "",
      "sensorid": "",
      "heater": undefined,
      "agitator": undefined,
    }
  }
  $scope.save = function() {


    console.log( $scope.selectedautomatic)
    if($scope.kettle.name.length == 0) {
      return;
    }
    CBPKettle.save($scope.kettle, function(data) {


      $scope.kettle = {
        "name": "",
        "sensorid": "",
        "heater": undefined,
        "agitator": undefined,
      }


      CBPKettle.query({}, function(response) {
        $scope.kettles = response.objects;
      });
    });
  }

}).controller('KettleEditController', function($scope, CBPKettle, $routeParams, CBPConfig, ConfirmMessage) {
  // Do something with myService
  $scope.vid = $routeParams.vid

    $scope.automatic = [];
    CBPKettle.get({
      "id": $scope.vid
    }, function(response) {
      $scope.kettle = response;
    });

    CBPKettle.getautomatic({}, function(response) {
      $scope.automatic = response;
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

    CBPKettle.getDevices({}, function(response) {
      angular.forEach(response, function(d) {
          $scope.gpio.push({"key":d, "value":d});
      })
    });

    $scope.save = function() {
      CBPKettle.update({
        "id": $scope.kettle.id
      }, $scope.kettle, function() {
        history.back();
      });
    }
    $scope.delete = function() {

      ConfirmMessage.open("Delete Kettle","Do you really want to delete the kettle?", function() {
        CBPKettle.delete({
          "id": $scope.kettle.id
        }, function() {
          history.back();
        });

      }, function() {

      });


    }
});
