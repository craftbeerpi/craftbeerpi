angular.module('craftberpi.controllers6', []).controller('SetupController', function(ws, $scope, $rootScope, $http, $uibModal, $location,  WizardHandler, CBPKettle) {


  $scope.num = 0


  $scope.gpio = []
  $scope.gpio.push({
    "key": undefined,
    "value": "NO GPIO",
  });
<<<<<<< HEAD
  for(i = 1; i < 31; i++) {
    $scope.gpio.push({
      "key": i,
      "value": i
    });
  }
=======

  CBPKettle.getDevices({}, function(response) {
    angular.forEach(response, function(d) {
        $scope.gpio.push({"key":d, "value":d});
    })
  });
>>>>>>> dev2.1

  $scope.thermometer = [];
  $scope.thermometer.push({"key":"", "value":"No Sensor"});

  CBPKettle.getthermometer({}, function(response) {
    angular.forEach(response, function(d) {
        $scope.thermometer.push({"key":d, "value":d});
    })
  });

  $scope.setup = function(num) {

    $scope.num = num
    $scope.kettles = [];
    for (i = 0; i < num; i++) {
      $scope.kettles.push({
        "name": "",
        "sensorid": "",
        "heater": undefined,
        "agitator": undefined,
      });
    }

    $scope.enterValidation = function() {
      var result = true;
      for (i = 0; i < $scope.kettles.length; i++) {
        if($scope.kettles[i].name == undefined ||   $scope.kettles[i].name == "") {
          result = false;
        }
      }
      return result;
    }

    WizardHandler.wizard().next();
  }

  $scope.finish = function() {
    var count = $scope.num;

    for (i = 0; i < $scope.kettles.length; i++) {
      CBPKettle.save($scope.kettles[i], function(data) {
          count--;
          if(count == 0)  {
            $location.url("/");
          }
      });
    }

  }


});
