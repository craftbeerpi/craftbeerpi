var app = angular.module('myApp', ['timer']);


app.controller('BrewController', ['ws', '$scope', '$http', function(ws, $scope, $http) {

    $scope.new_target_temp = {}
    $scope.vessel = []
    $scope.vessel_temps = {}
    $scope.vessel_temp_log = {}

    $http.get('/vessel/data').
      success(function(data, status, headers, config) {
        $scope.vessel = data.vessel;
        $scope.vessel_temps = data.vessel_temps;
        $scope.vessel_temp_log = data.vessel_temp_log;
    }).
    error(function(data, status, headers, config) {
        // log error
    });

    $http.get('/steps/steps').
      success(function(data, status, headers, config) {
        $scope.steps = data;
    }).
    error(function(data, status, headers, config) {
        // log error
    });

    $scope.buttonState = function(state) {
        if(state == true) {
            return "btn-success"
        }
        else {
            return "btn-default"
        }
    }

    $scope.stepStyle = function(item) {


        if (item.state == "D")
            return "info";
        else if (item.type == "M" && item.state == "A" && $scope.temp < item.temp) {
            return "warning"
        }
        else if (item.type == "M" && item.state == "A" && $scope.vessel_temps[item["vesselid"]][1]>= item.temp) {
          return "active"
        }
        else if (item.state == "A" && item.timer_start != null) {
            return "active"
        }
        else if (item.state == "A" && item.timer_start == null) {
            return "warning"
        }
        else
            return "";
    }

    $scope.stateClassIcon = function(item) {
        if (item.state == "A")
            return "fa fa-spinner fa-spin"
        else if (item.state == "D")
            return "fa fa-check";
        else
            return "";
    }

    $scope.vesselState = function(vid) {

      if($scope.steps == undefined) {
        return;
      }

      for(i = 0; i < $scope.steps.length; i++) {
        if($scope.steps[i].state == "A" && vid == $scope.steps[i].vesselid) {
          return "active"
        }
      }
    }

    $scope.calc1MinAvg = function(vid) {
      if($scope.vessel_temp_log[vid] != undefined && $scope.vessel_temp_log[vid].length >= 12) {
        temp_1_min_ago =  $scope.vessel_temp_log[vid][$scope.vessel_temp_log[vid].length - 12][1];
        temp = $scope.vessel_temps[vid][1]
        //console.log("LENGHT " + $scope.vessel_temp_log[vid].length + "OLD TEMP: " + temp_1_min_ago + " TEMP: " +temp);

        return (temp - temp_1_min_ago).toFixed(2);
      }
    }

    $scope.vessel_update = function(data) {
        $scope.vessel = data;
    }

    $scope.vessel_temp_update = function(data) {
        $scope.vessel_temps = data;
    }

    $scope.vessel_automatic_on = function(data) {
        $scope.vessel[data].heater.state = true;
    }

    $scope.vessel_automatic_off = function(data) {
        $scope.vessel[data].heater.state = false;
    }

    $scope.vessel_gpio = function(gpio) {
        ws.emit("vessel_gpio", gpio)
    }

    $scope.vessel_automatic = function(vesselid) {
        ws.emit("vessel_automatic", vesselid)
    }

    $scope.next = function() {
       ws.emit("next");
    }

    $scope.start = function() {
       ws.emit("start");
    }

    $scope.reset = function() {
        ws.emit("reset");
    }

    $scope.updateSteps = function(data) {
        $scope.steps = data;
    }

    $scope.setTargetTemp = function(vesselid) {

       ws.emit("vessel_set_target_temp", {"vesselid": vesselid, "temp":  $scope.new_target_temp[vesselid]});
       $scope.new_target_temp[vesselid] = undefined;
    }

    ws.on('vessel_update', $scope.vessel_update);
    ws.on('vessel_temp_update', $scope.vessel_temp_update);
    ws.on('vessel_automatic_on', $scope.vessel_automatic_on);
    ws.on('vessel_automatic_off', $scope.vessel_automatic_off);
    ws.on('steps', $scope.updateSteps);
}]);

app.factory('ws', ['$rootScope', function($rootScope) {
    'use strict';

    var socket = io.connect('/brew');
    socket.on('connect', function(msg) {
        console.log("connect");
    });

    return {

        on: function(event, callback) {

            socket.on(event, function(data) {
                $rootScope.$apply(function() {
                    callback(data);
                });

            });
        },
        emit: function(event, data) {
            if(data == undefined) {
                socket.emit(event);
            }
            else {
                socket.emit(event, data);
            }

        }
    }
}]);
