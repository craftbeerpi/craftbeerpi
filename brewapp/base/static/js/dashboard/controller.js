angular.module('myApp.controllers2', []).controller('DashBoardController', function($scope, $location, CBPSteps, CBPKettle, $uibModal, ws) {

  CBPKettle.query(function(data) {
      $scope.kettles = data.objects;
  });

  CBPSteps.query(function(data) {
      $scope.steps = data.objects;
  });

  CBPKettle.getstate(function(data) {
      $scope.kettle_state = data;
  });

  $scope.getTemp = function(item) {
    if($scope.kettle_state == undefined) {
      return ""
    }
    else {
      return $scope.kettle_state[item.id]['temp'];
    }
  }
  $scope.buttonState = function(item, element) {
    var state = false;

    if($scope.kettle_state == undefined) {
      return "btn-default"
    }
    if($scope.kettle_state[item.id][element]) {
        state = $scope.kettle_state[item.id][element]['state'];
        if (state == true) {
          return "btn-success"
        } else {
          return "btn-default"
        }
    }
  }
  $scope.kettleState = function(vid) {
    if ($scope.steps == undefined) {
      return;
    }
    for (i = 0; i < $scope.steps.length; i++) {
      if ($scope.steps[i].state == "A" && vid == $scope.steps[i].kettleid) {
        return "panel-success"
      }
    }
  }

  $scope.stepStyle = function(item) {

    //var num_of_kettles = Object.keys($scope.kettle_temps).length;
    num_of_kettles = 1;

    if (item.state == "D")
      return "info";
    else if (item.type == "M" && item.state == "A" && $scope.temp < item.temp) {
      return "warning"
    } else if (item.type == "M" && item.state == "A" && num_of_kettles > 0 && $scope.kettle_temps[item["kettleid"]][1] >= item.temp) {
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
        kettle: function() {
          return item
        }
      }
    });

    modalInstance.result.then(function(target_temp) {
      if (target_temp != undefined) {
        ws.emit("kettle_set_target_temp", {
          "kettleid": item.id,
          "temp": target_temp
        });
      }

    }, function() {
      console.log("dismiss");
    });
  };

  $scope.calcVolume = function(item) {
    var modalInstance = $uibModal.open({
      animation: true,
      templateUrl: '/base/static/partials/dashboard/volume.html',
      controller: 'VolumeController',
      size: "sm",
      resolve: {
        kettle: function() {
          return item
        }
      }
    });

    modalInstance.result.then(function(target_temp) {
      /*if (target_temp != undefined) {
        ws.emit("kettle_set_target_temp", {
          "kettleid": item.id,
          "temp": target_temp
        });
      }
*/
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



  $scope.kettle_update = function(data) {
    $scope.kettles = data;
  }

  $scope.kettle_state_update = function(data) {
    $scope.kettle_state = data;
  }

  $scope.step_update = function(data) {
    $scope.steps = data;
  }

  ws.on('kettle_state_update', $scope.kettle_state_update);
  ws.on('kettle_update', $scope.kettle_update);
  ws.on('step_update', $scope.step_update);

}).controller('TargetTempController', function($scope, $uibModalInstance, kettle) {

  $scope.target_temp = undefined;
  $scope.kettle = kettle;
  $scope.ok = function() {
    $uibModalInstance.close($scope.target_temp);
  };

  $scope.cancel = function() {
    $uibModalInstance.dismiss('cancel');
  };
}).controller('VolumeController', function($scope, $uibModalInstance, kettle) {

  $scope.target_temp = undefined;
  $scope.kettle = kettle;
  $scope.ok = function() {
    $uibModalInstance.close($scope.target_temp);
  };

  $scope.cancel = function() {
    $uibModalInstance.dismiss('cancel');
  };
});
