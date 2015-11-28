var app = angular.module('myApp', ['timer']);




app.controller('ArticlesCtrl', ['ws', '$scope', '$http', function(ws, $scope, $http) {

    $scope.temp = "---";
    $scope.steps = [];
    $scope.data = [];
    $scope.log = [];

    $scope.gpiosState = {};
    $scope.pidState = false;

    $scope.addlog = function() {

        if($scope.message != undefined && $scope.message.length > 0 )
        {
             ws.emit("addlog", $scope.message);
             $scope.message = "";
        }


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

    $scope.whatClassIsIt = function(item) {

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

    $http.get('/data').
    success(function(data, status, headers, config) {

        console.log();

        var keys = Object.keys(data.chart);

        $scope.agitatorState = data.agitator;
        $scope.heatingState = data.heating;
        $scope.pidState = data.pid;
        $scope.temp = data.temps["temp1"][1].toFixed(2);
        $scope.auto = data.auto;
        $scope.steps = data.steps;
        $scope.data = data.chart;
        $scope.log = data.logs
        $scope.brew_name = data.brew_name
        //$scope.gpiosState = data.gpio;

        $scope.gpios = data.gpios;
        $scope.point = data.point;


        $scope.axis_config = {}
        chart_data = [];
        for (var i=0; i < keys.length; i++) {
            k =keys[i];

            $scope.axis_config[k] = 'x'+i
            chart_data = chart_data.concat($scope.downsample(data.chart[k], k, "x"+i));

        }


        //chart_data = $scope.downsample(data.chart["temp1"], "temp", "x1");

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

    $scope.agitatorupdate = function(data) {
        $scope.agitatorState =  data
    }

    $scope.heatingState = function(data) {
        $scope.heatingState =  data
    }

    $scope.pidState = function(data) {
        $scope.pidState =  data
    }

    $scope.point = function(data) {
        $scope.point =  data
    }


    $scope.cud = function(data) {

        chart_data = [];
        $scope.temp = data["temp1"][0][1].toFixed(2);
        var keys = Object.keys($scope.axis_config);
        for (var i=0; i < keys.length; i++) {
          d = keys[i];
          x = $scope.axis_config[keys[i]];

          $scope.chart.flow({
            columns: [[x, data[d][0][0]], [d, data[d][0][1]]],
            length: 0,
          });
        }



    }

    $scope.alert = function(data) {
        console.log("alert");
        var a = new Audio("static/sound.mp3");
        a.play();
    }

    ws.on('point', $scope.point);
    ws.on('temp', $scope.update);
    ws.on('alert', $scope.alert);
    ws.on('chart_update', $scope.cud);
    ws.on('steps', $scope.updateSteps);
    ws.on('logupdate', $scope.updateLog);
    ws.on('pidupdate', $scope.pidState);
    ws.on('gpio_update', $scope.gpio_update);

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
