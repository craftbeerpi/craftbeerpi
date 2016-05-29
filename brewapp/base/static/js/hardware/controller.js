angular.module('craftbeerpi.hardware', []).controller('PumpOverviewController', function($scope, $location, CBPHardware, ConfirmMessage,$uibModal, CBPKettle, CBPConfig) {

  // available types
  $scope.type = [
    {"key":"P", "value": "Pump"},
    {"key":"A", "value": "Agitator"},
    {"key":"H", "value": "Heater"},
    {"key":"O", "value": "Other"},
  ];

  // Get GPIOs
  $scope.gpio = []
  CBPKettle.getDevices({}, function(response) {
    angular.forEach(response, function(d) {
      $scope.gpio.push({
        "key": d,
        "value": d
      });
    })
  });

  // load current hardware
  CBPHardware.query(function(response) {
    $scope.hw = response.objects;
  });

  // modal dialog for new hardware
  $scope.createHardware = function() {
    var modalInstance = $uibModal.open({
      animation: true,
      controller: "HardwareCreateController",
      scope: $scope,
      templateUrl: '/base/static/partials/hardware/form.html',
      size: "sm"
    });
    modalInstance.result.then(function(data) {
      CBPHardware.query(function(response) {
        $scope.hw = response.objects;
      });
    });
  }

  // modal dialog to edit existing hardware
  $scope.edit = function(id) {
    $scope.selected = id
    var modalInstance = $uibModal.open({
      animation: true,
      controller: "HardwareEditController",
      scope: $scope,
      templateUrl: '/base/static/partials/hardware/form.html',
      size: "sm"
    });
    modalInstance.result.then(function(data) {
      CBPHardware.query(function(response) {
        $scope.hw = response.objects;
      });
    });
  }

  $scope.hardwareType = function(s) {
    switch (s) {
      case "H":
        return "fa-fire";
        break;
      case "A":
        return "fa-refresh";
        break;
      case "P":
        return "fa-tint"
        break;
      default:
        return "fa-plug"
        break;
    }
  }

})
.controller("HardwareCreateController", function($scope, CBPHardware, $uibModalInstance) {
  $scope.edit=false;

  $scope.hardware = {
      "name": "",
      "config": {
        "inverted": false,
        "hide": false
      }

  };

  $scope.save = function() {
    if ($scope.hardware.name.length == 0) {
      return;
    }

    CBPHardware.save($scope.hardware, function(data) {
        $uibModalInstance.close();
    });
  }
  $scope.cancel = function() {
    $uibModalInstance.dismiss('cancel');
  };

}).controller('HardwareEditController', function($scope, CBPHardware, ConfirmMessage,$uibModalInstance, CBPKettle) {

  $scope.edit=true;
  CBPHardware.get({
    "id": $scope.selected
  }, function(response) {
    $scope.hardware = response;
  });

  $scope.save = function() {
    console.log("SAVE");
    console.log($scope.hardware);
    CBPHardware.update({
      "id": $scope.hardware.id
    }, $scope.hardware, function() {
      $uibModalInstance.close({});
    });
  }

  $scope.delete = function() {
    ConfirmMessage.open("Delete Hardware","Do you really want to delete the hardware?", function() {
      CBPHardware.delete({
        "id": $scope.hardware.id
      }, function() {
            $uibModalInstance.close();
      });
    }, function() { });
  }
  $scope.cancel = function() {
    $uibModalInstance.dismiss('cancel');
  };
});
