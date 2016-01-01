var app = angular.module('myApp', ['timer']);




app.controller('BrewController', ['ws', '$scope', '$http', function(ws, $scope, $http) {

    $scope.temp = "---";
    $scope.steps = [];
    $scope.data = [];
    $scope.log = [];
    $scope.temps = {};


    $scope.addlog = function() {
        if($scope.message != undefined && $scope.message.length > 0 )
        {
             ws.emit("addlog", $scope.message);
             $scope.message = "";
        }
    }

    $scope.debug = function() {
      $http.get('/base/data').
      success(function(data, status, headers, config) {

          console.log(data);
          $scope.configdata = data;
        });
    }

    $scope.gpio = function(item) {
        ws.emit("gpio", item)
    }


    $scope.gpioState = function(item) {
        if($scope.gpios == undefined) {
            return false;
        }
        for (var i = 0; i < $scope.gpios.length; i++) {
            if($scope.gpios[i].id == item) {
                return $scope.gpios[i].state;
            }
        }
    }

    $scope.buttonState = function(item) {
        if(item.state == true) {
            return "btn-success"
        }
        else {
            return "btn-default"
        }
    }

    $scope.stepStyle = function(item) {

        if (item.state == "D")
            return "info";
        else if (item.type == "M" && item.state == "A" && $scope.temp < item.temp)
            return "warning"
        if (item.type == "M" && item.state == "A" && $scope.temp >= item.temp)
            return "active"
        else if (item.state == "A" && item.timer_start != null)
            return "active"
        else if (item.state == "A" && item.timer_start == null)
            return "warning"

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

    $scope.started = function() {
        if($scope.steps == undefined) {
          return false;
        }
        for(i = 0; i < $scope.steps.length; i++) {
          if($scope.steps[i].state == "A") {
            return true;
          }
        }
        return false;
    }

    $http.get('/base/data').
      success(function(data, status, headers, config) {

        console.log(data);
        $scope.configdata = data;
        $scope.steps = data.steps;
        $scope.gpios = data.gpio;
        $scope.thermometer = data.thermometer;
        $scope.log = data.log;
        /*
        var keys = Object.keys(data.chart);
        $scope.agitatorState = data.agitator;
        $scope.heatingState = data.heating;
        $scope.pidState = data.pid;
        $scope.temp = data.temps["temp1"][1].toFixed(2);
        $scope.auto = data.auto;

        $scope.data = data.chart;
        $scope.log = data.logs
        $scope.brew_name = data.brew_name
        //$scope.gpiosState = data.gpio;

        $scope.gpios = data.gpios;
*/

        var keys = Object.keys(data.chart);

        $scope.axis_config = {}
        chart_data = [];
        for (var i=0; i < keys.length; i++) {
            k =keys[i];
            $scope.axis_config[k] = k+"x";

            chart_data = chart_data.concat($scope.downsample(data.chart[k], k, k+"x"));

        }

        $scope.chart = c3.generate({
                bindto: '#chart',
                data: {
                    xs: $scope.axis_config ,
                    columns: chart_data,
                    type: 'area',

                },
                point: {
                    show: false
                },
                legend: {
                    show: false
                },
                axis: {
                    x: {
                        type: 'timeseries',
                        tick: {
                            format: '%H:%M:%S',
                            count: 10
                        },
                        label: 'Zeit'
                    },
                    y: {
                        label: 'Temperatur',
                        max: 110,
                        min: 10,
                    },

                }

            }
        );


    }).
    error(function(data, status, headers, config) {
        // log error
    });


    $scope.downsample = function(data, x, y) {


        if (typeof(x)==='undefined') x = "P1";
        if (typeof(y)==='undefined') y = "x";

        if(data ==undefined) {
            return
        }

        names = [[y, x]];
        var down = largestTriangleThreeBuckets(data, 250, 0, 1);


        p1 = [x];
        x = [y];


        for (var i = 0; i < down.length; i++) {

            p1.push(down[i][1]);
            x.push(down[i][0]);
        }
        return [p1, x];
    }

    $scope.reset = function() {
        ws.emit("reset");
    }

    $scope.next = function() {

       ws.emit("next");

    }

    $scope.start = function() {
       ws.emit("start");
    }

    $scope.switchauto = function() {
        ws.emit("auto");
    }

    $scope.pid = function() {
        ws.emit("pid");
    }

    $scope.updateSteps = function(data) {
        $scope.steps = data;
    }

    $scope.updateLog = function(data) {
        $scope.log.push(data)
    }

    $scope.gpio_update = function(data) {

        $scope.gpios = data;
    }

    $scope.gpio2 = function(data) {

        console.log(data);
    }

    $scope.agitatorupdate = function(data) {
        $scope.agitatorState =  data
    }

    $scope.heatingState = function(data) {
        $scope.heatingState =  data
    }

    $scope.pidState = function(data) {
        $scope.pidState =  data
    }

    $scope.cud = function(data) {

        console.log(data);
        $scope.temps = data;
        chart_data = [];
        $scope.temp = data.value1[1].toFixed(2);
        //var keys = Object.keys($scope.axis_config);
        //for (var i=0; i < keys.length; i++) {
        //  d = keys[i];
        //  x = $scope.axis_config[keys[i]];

        var updateData = [];
        for (var key in $scope.axis_config) {
          console.log(key);
          updateData.push([key+"x",data[key][0]]);
          updateData.push([key,data[key][1]]);
        }

        console.log(updateData);



        $scope.chart.flow({
            columns: updateData,
            length: 0
          });
        //}
    }

    $scope.alert = function(data) {
        console.log("alert");
        var a = new Audio("static/sound.mp3");
        a.play();
    }

    ws.on('temp', $scope.update);
    ws.on('alert', $scope.alert);
    ws.on('chart_update', $scope.cud);
    ws.on('steps', $scope.updateSteps);
    ws.on('logupdate', $scope.updateLog);
    ws.on('pidupdate', $scope.pidState);
    ws.on('gpio_update', $scope.gpio_update);
    ws.on('gpio', $scope.gipo2);
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
