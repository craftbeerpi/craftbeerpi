var app = angular.module('brewApp', [])

app.controller('BrewController', ['ws', '$scope', '$http', function(ws, $scope, $http) {

  $scope.height = 40;
  $scope.diameter = 30;

  function Round(v) {
    return ("" + (Math.round(v * 100) / 100)).replace(/\./g, ",");
  }

  $scope.volume = function() {

    var height = parseFloat($scope.height);
    var radius = parseFloat($scope.diameter) / 2.0;
    return Round(Math.PI * radius * radius * height / 1000.0);
  }






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
