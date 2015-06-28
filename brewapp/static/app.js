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
            return "btn-danger"
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


    $scope.chart = c3.generate({
            bindto: '#chart',
            data: {
                xs: {
                    temp: 'x1',
                },
                //xFormat: '%Y-%m-%d %H:%M:%S',
                type: 'area',
                columns: [
                    ['temp', 0],
                    ['x1', 0],
                ],
                

            },
            point: {
                show: false
            },
            axis: {
                x: {
                    type: 'timeseries',
                    tick: {
                        format: '%H:%M:%S',
                        count: 50
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

    $http.get('/data').
    success(function(data, status, headers, config) {


        $scope.agitatorState = data.agitator;
        $scope.heatingState = data.heating;
        $scope.pidState = data.pid;
        $scope.temp = data.temp;
        $scope.auto = data.auto;
        $scope.steps = data.steps;
        $scope.data = data.temps;
        $scope.log = data.logs
        $scope.brew_name = data.brew_name
        //$scope.gpiosState = data.gpio;
      
        $scope.gpios = data.gpios;
        chart_data = $scope.downsample(data.temps, "temp", "x1");        

        $scope.chart.load({
            columns: chart_data,
            length: 0
        });
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

    $scope.update = function(value) {

        $scope.temp = value.temp.toFixed(2);
        $scope.data.push([value.time, value.temp]);

        $scope.chart.load({
            columns: $scope.downsample($scope.data, "temp", "x1"),
            length: 0
        });
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

    ws.on('temp', $scope.update);
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