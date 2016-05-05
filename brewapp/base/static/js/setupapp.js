var $setup = angular.module('craftbeerpisetup',
['mgo-angular-wizard',
'pascalprecht.translate']).config(['$translateProvider', function ($translateProvider) {
  // configures staticFilesLoader
  $translateProvider.useStaticFilesLoader({
    prefix: "/static/languages/",
    suffix: ".json"
  });
  // load 'en' table on startup
  $translateProvider.preferredLanguage('en');
}]);

$setup.controller("SetupController", function($scope, $location, $window, $http,WizardHandler) {

  console.log("SETUP")



  $scope.setup = function(id) {

    WizardHandler.wizard().next();
  }

  $scope.selectHardware = function(type) {
      $http({
        method: 'POST',
        url: '/api/setup/hardware',
        data: { 'type': type }
      }).then(function successCallback(response) {
          $scope.gpio = []
          $scope.gpio.push({
            "key": undefined,
            "value": "NO GPIO",
          });
          angular.forEach(response.data, function(d) {
              $scope.gpio.push({"key":d, "value":d});
          });
        }, function errorCallback(response) {

        });
      WizardHandler.wizard().next();
  }

  $scope.selectThermometer = function(type) {
    $http({
      method: 'POST',
      url: '/api/setup/thermometer',
      data: { 'type': type }
    }).then(function successCallback(response) {
        $scope.thermometer = [];
        $scope.thermometer.push({"key":"", "value":"No Sensor"});
        angular.forEach(response.data, function(d) {
            $scope.thermometer.push({"key":d, "value":d});
        });
      }, function errorCallback(response) {

      });
      WizardHandler.wizard().next();
  }

  $scope.selectkettle = function(num) {
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
    WizardHandler.wizard().next();
  }



$scope.finish = function() {

      $http({
        method: 'POST',
        url: '/api/setup/kettle',
        data: { 'kettles': $scope.kettles }
      }).then(function successCallback(response) {
            $window.location.href = '/';
        }, function errorCallback(response) {

        });


}
});
