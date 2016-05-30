var $setup = angular.module('craftbeerpisetup',
['mgo-angular-wizard',
'ngCookies','ui.bootstrap',
'pascalprecht.translate']).config(['$translateProvider', function ($translateProvider) {
  // configures staticFilesLoader
  $translateProvider.useStaticFilesLoader({
    prefix: '/static/languages/',
    suffix: '.json'
  }).fallbackLanguage('en');
  $translateProvider.useCookieStorage();
  $translateProvider.determinePreferredLanguage()
}]);

$setup.controller("SetupController", function($scope, $translate, $location, $window, $http,WizardHandler) {


  $scope.language= $translate.proposedLanguage();

  $scope.type = [
    {"key":"P", "value": "Pump"},
    {"key":"A", "value": "Agitator"},
    {"key":"H", "value": "Heater"},
    {"key":"O", "value": "Other"},
  ];

  $scope.hardware = [{"name": "", "config": {"inverted": false, "hide": false}}];



  $scope.addHardware = function () {
      $scope.hardware.push({"name": "", "config": {"inverted": false, "hide": false}});
  };
  $scope.removeHardware = function (index) {
      console.log(index);
      $scope.hardware.splice( index, 1 );
  };



  $scope.setup = function(id) {
    WizardHandler.wizard().next();
  }

  $scope.changeLanguage = function (langKey) {
    console.log("OK");
    $scope.language=langKey;
    $translate.use(langKey);
  };

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
    $scope.num = num;

    $scope.heater = []
    $scope.heater.push({
      "key": undefined,
      "value": "NO HARDWARE",
    });

    $scope.agitator = []
    $scope.agitator.push({
      "key": undefined,
      "value": "NO HARDWARE",
    });

    $scope.hardware.forEach(function(entry) {
      console.log(entry)
      if(entry.type == "H") {
        $scope.heater.push({
          "key": entry.switch,
          "value": entry.name
        });
      }
      if(entry.type == "A") {
        $scope.agitator.push({
          "key": entry.switch,
          "value": entry.name
        });
      }
    });

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
        data: { 'kettles': $scope.kettles , 'hardware': $scope.hardware}
      }).then(function successCallback(response) {
            $window.location.href = '/';
        }, function errorCallback(response) {

        });


}
});
