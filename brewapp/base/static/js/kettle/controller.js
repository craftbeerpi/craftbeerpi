angular.module('craftbeerpi.kettle', []).controller('KettleOverviewController', function($scope, $location, CBPSteps, CBPKettle, CBPHardware, $uibModal, ConfirmMessage, CBPConfig) {

  CBPKettle.query({}, function(response) {
    $scope.kettles = response.objects
  });

  $scope.thermometer = [];
  $scope.thermometer.push({
    "key": "",
    "value": "No Thermometer"
  });

  CBPKettle.getthermometer({}, function(response) {
    angular.forEach(response, function(d) {
      $scope.thermometer.push({
        "key": d,
        "value": d
      });
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
    "target_temp": 0
  }

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



  CBPHardware.query(function(data) {
    data.objects.forEach(function(entry) {
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


  });

  $scope.getHardwareName = function(data, gpio) {

      try {

          for(var i = 0; i < data.length; i++) {
            if(data[i].key == gpio) {
              return data[i].value;
            }
          }
      }
      catch(e) {
        return
      }

  }

  $scope.clearTempLogs = function() {
    ConfirmMessage.open("Clear Temperature Log", "Do you really want to clear all Temperature Logs?", function() {
      CBPKettle.clear({}, function(response) {
      });
    }, function() {});
  }

  $scope.create = function() {
    var modalInstance = $uibModal.open({
      animation: true,
      controller: "KettleNewController",
      scope: $scope,
      templateUrl: '/base/static/partials/kettle/form.html',
      size: "lg"
    });
    modalInstance.result.then(function(data) {
      CBPKettle.query({}, function(response) {
        $scope.kettles = response.objects;
      });
    });
  }

  $scope.edit = function(id) {
    $scope.selected = id
    var modalInstance = $uibModal.open({
      animation: true,
      controller: "KettleEditController",
      scope: $scope,
      templateUrl: '/base/static/partials/kettle/form.html',
      size: "lg",
      resolve: {"id": id}
    });
    modalInstance.result.then(function(data) {
      CBPKettle.query({}, function(response) {
        $scope.kettles = response.objects;
      });
    });
  }

}).
controller('KettleNewController', function($scope, $uibModalInstance, CBPKettle) {
  $scope.edit = false;
  $scope.cancel = function() {
    $uibModalInstance.dismiss('cancel');
  };

  $scope.save = function() {
    if ($scope.kettle.name.length == 0) {
      return;
    }
    CBPKettle.save($scope.kettle, function(data) {
      $scope.kettle = {
        "name": "",
        "sensorid": "",
        "heater": undefined,
        "agitator": undefined,
      }
      $uibModalInstance.close({});
    });
  }

}).controller('KettleEditController', function($scope, CBPKettle, $routeParams, CBPConfig, ConfirmMessage, $uibModalInstance) {


  $scope.edit = true;
  CBPKettle.get({
    "id": $scope.selected
  }, function(response) {
    $scope.kettle = response;
  });
  $scope.save = function() {
    console.log($scope.kettle.name)
    if ($scope.kettle.name.length == 0) {
      return;
    }
    CBPKettle.update({
      "id": $scope.kettle.id
    }, $scope.kettle, function() {
      $uibModalInstance.close({});
    });
  }
  $scope.delete = function() {
    ConfirmMessage.open("Delete Kettle", "Do you really want to delete the kettle?", function() {
      CBPKettle.delete({
        "id": $scope.kettle.id
      }, function() {
        $uibModalInstance.close({});
      });
    }, function() {
    });
  }
  $scope.cancel = function() {
    $uibModalInstance.dismiss('cancel');
  };
});
