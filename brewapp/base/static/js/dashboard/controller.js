angular.module('myApp.controllers2', []).controller('DashBoardController', function($scope, $location, CBPSteps, CBPVessel, $uibModal, ws) {

  CBPVessel.query(function(data) {
      $scope.vessels = data.objects;
  });

  CBPSteps.query(function(data) {
      $scope.steps = data.objects;
  });

  CBPVessel.getstate(function(data) {
      $scope.vessel_state = data;
  });

  $scope.getTemp = function(item) {
    if($scope.vessel_state == undefined) {
      return ""
    }
    else {
      return $scope.vessel_state[item.id]['temp'];
    }
  }
  $scope.buttonState = function(item, element) {
    var state = false;

    if($scope.vessel_state == undefined) {
      return "btn-default"
    }
    if($scope.vessel_state[item.id][element]) {
        state = $scope.vessel_state[item.id][element]['state'];
        if (state == true) {
          return "btn-success"
        } else {
          return "btn-default"
        }
    }
  }
  $scope.vesselState = function(vid) {
    if ($scope.steps == undefined) {
      return;
    }
    for (i = 0; i < $scope.steps.length; i++) {
      if ($scope.steps[i].state == "A" && vid == $scope.steps[i].vesselid) {
        return "panel-success"
      }
    }
  }

  $scope.stepStyle = function(item) {

    //var num_of_vessels = Object.keys($scope.vessel_temps).length;
    num_of_vessels = 1;

    if (item.state == "D")
      return "info";
    else if (item.type == "M" && item.state == "A" && $scope.temp < item.temp) {
      return "warning"
    } else if (item.type == "M" && item.state == "A" && num_of_vessels > 0 && $scope.vessel_temps[item["vesselid"]][1] >= item.temp) {
      return "active"
    } else if (item.state == "A" && item.timer_start != null) {
      return "active"
    } else if (item.state == "A" && item.timer_start == null) {
      return "warning"
    } else
      return "";
  }

  $scope.reset = function() {
    console.log("RESET");
    ws.emit("reset");
  }

  $scope.next = function() {
    console.log("NEXT STEP");
    ws.emit("next");
  }

  $scope.start = function() {
    console.log("START");
      ws.emit("start");
  }

  $scope.setTargetTemp = function(item) {
    var modalInstance = $uibModal.open({
      animation: true,
      templateUrl: '/base/static/partials/dashboard/target_temp.html',
      controller: 'TargetTempController',
      size: "sm",
      resolve: {
        vessel: function() {
          return item
        }
      }
    });

    modalInstance.result.then(function(target_temp) {
      if (target_temp != undefined) {
        ws.emit("vessel_set_target_temp", {
          "vesselid": item.id,
          "temp": target_temp
        });
      }

    }, function() {
      console.log("dismiss");
    });
  };


  $scope.switchGPIO = function(item, element) {
    ws.emit("switch_gipo", {
      "vid": item.id,
      "element": element,
      "state": true
    });
  }



  $scope.vessel_update = function(data) {
    $scope.vessels = data;
  }

  $scope.vessel_state_update = function(data) {
    $scope.vessel_state = data;
  }

  $scope.step_update = function(data) {
    $scope.steps = data;
  }

  ws.on('vessel_state_update', $scope.vessel_state_update);
  ws.on('vessel_update', $scope.vessel_update);
  ws.on('step_update', $scope.step_update);

}).controller('TargetTempController', function($scope, $uibModalInstance, vessel) {

  $scope.target_temp = undefined;
  $scope.vessel = vessel;
  $scope.ok = function() {
    $uibModalInstance.close($scope.target_temp);
  };

  $scope.cancel = function() {
    $uibModalInstance.dismiss('cancel');
  };
});
