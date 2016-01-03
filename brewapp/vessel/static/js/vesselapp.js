var app = angular.module('BrewApp', ['timer','ui.bootstrap', 'ngRoute']).config(function($routeProvider) {
  $routeProvider
    .when('/', { templateUrl: 'static/vessel_overview.html', name:"Dashboard" })
    .when('/chart/:vid', { templateUrl: 'static/chart.html' })
    .when('/formulas', { templateUrl: 'static/volume.html' })
    .when('/steps_settings', { templateUrl: 'static/steps_settings.html' })
    .when('/vessel_settings', { templateUrl: 'static/vessel_settings_overview.html', name:"Vessel Settings" })
    .when('/vessel_settings/:vid', { templateUrl: 'static/vessel_settings.html'})
    .when('/about', { templateUrl: 'static/about.html', name: "About"})
    .when('/volumes/:vid', { templateUrl: 'static/volume.html' })
    .otherwise({ redirectTo: '/'});
});


app.factory('routeNavigation', function($route, $location) {
  var routes = [];
  angular.forEach($route.routes, function (route, path) {
    if (route.name) {
      routes.push({
        path: path,
        name: route.name
      });
    }
  });
  return {
    routes: routes,
    activeRoute: function (route) {
      return route.path === $location.path();
    }
  };
});

app.factory('Vessel', ['$http', function($http) {

  var vessel = {}
    return {
      init: function() {

        $http.get('/vessel/data').
          success(function(data, status, headers, config) {
            vessel = data.vessel;
        }).
        error(function(data, status, headers, config) {
            // log error
        });
      },
      getVessels: function() {
        return vessel;
      },
      setVessels: function(v) {
        vessel = v;
      }
    };
}]);


app.directive('navigation', function (routeNavigation) {
  return {
    restrict: "E",
    replace: true,
    templateUrl: "static/navigation-directive.tpl.html",
    controller: function ($scope) {
      $scope.routes = routeNavigation.routes;
      $scope.activeRoute = routeNavigation.activeRoute;
    }
  };
});


app.directive( 'backButton', function() {
    return {
        restrict: 'A',
        link: function( scope, element, attrs ) {
            element.on( 'click', function () {
                history.back();
                scope.$apply();
            } );
        }
    };
} );

app.controller('TargetTempCtrl', function ($scope, $uibModalInstance, vessel) {

  $scope.target_temp = undefined;
  $scope.vessel = vessel;
  $scope.ok = function () {
    $uibModalInstance.close($scope.target_temp);
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
});

app.controller('ChartController', ['ws', '$scope', '$http', 'Vessel', '$routeParams', function(ws, $scope, $http, Vessel, $routeParams) {

    $scope.load = function() {

    $scope.vessel_name = Vessel.getVessels()[$routeParams.vid];

    $http.get('/vessel/chartdata/'+$routeParams.vid).
      success(function(data, status, headers, config) {
        var chart_data = $scope.downsample(data, "daten", "x");
        $scope.chart = c3.generate({
                bindto: '#chart',
                data: {
                    xs: {daten: "x"} ,
                    columns: chart_data,
                    type: 'area',

                },
                point: {
                    show: false
                },
                legend: {
                    show: false
                },
                grid: {
                  x: {
                    show: true
                  },
                  y: {
                    show: true
                  }
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
    }

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

      $scope.load();
}]);

app.controller('FormularController', ['ws', '$scope', '$http', '$routeParams', function(ws, $scope, $http, $routeParams) {

  $scope.vessel_name = "";
  $scope.height = 0;
  $scope.diameter = 0;
  $scope.free = 0;
  $http.get('/vessel/vessel/'+$routeParams.vid).
    success(function(data, status, headers, config) {
      $scope.height = data.height;
      $scope.vessel_name = data.name
      $scope.diameter = data.diameter;
  }).
  error(function(data, status, headers, config) {
      // log error
  });

  function Round(v) {
    return ("" + (Math.round(v * 100) / 100)).replace(/\./g, ",");
  }
  $scope.volume = function() {
    var maxHeight = parseFloat($scope.height);
    var free = parseFloat($scope.free);
    var height = maxHeight - free;
    var radius = parseFloat($scope.diameter) / 2.0;
    return Round(Math.PI * radius * radius * height / 1000.0);
  }
  $scope.maxvolume = function() {
    var maxHeight = parseFloat($scope.height);
    var free = parseFloat($scope.free);
    var radius = parseFloat($scope.diameter) / 2.0;
    return Round(Math.PI * radius * radius * maxHeight / 1000.0);
  }
}]);

app.controller('VesselOverviewController', ['ws', '$scope', '$http', 'Vessel', '$uibModal', function(ws, $scope, $http, Vessel, $uibModal) {
    $scope.vessels = Vessel.getVessels();
}]);

app.controller('VesselController', ['ws', '$scope', '$http', 'Vessel', '$uibModal', '$routeParams', function(ws, $scope, $http, Vessel, $uibModal, $routeParams) {

    $scope.vessel = Vessel.getVessels()[$routeParams.vid];
}]);


app.controller('BrewController', ['ws', '$scope', '$http', 'Vessel', '$uibModal', function(ws, $scope, $http, Vessel, $uibModal) {
    $scope.new_target_temp = {}
    $scope.vessel = []
    $scope.vessel_temps = {}
    $scope.vessel_temp_log = {}
    $scope.target_temp = undefined;
    $scope.open = function (vid, size) {


    var modalInstance = $uibModal.open({
      animation: true,
      templateUrl: 'static/target_temp.html',
      controller: 'TargetTempCtrl',
      size: size,
      resolve: {
        vessel: function () {
          return $scope.vessel[vid];
        }
      }
    });

    modalInstance.result.then(function (target_temp) {
      if(target_temp != undefined) {
            ws.emit("vessel_set_target_temp", {"vesselid": vid, "temp":  target_temp});
      }

    }, function () {
      console.log("dismiss");
    });
  };


    $http.get('/vessel/data').
      success(function(data, status, headers, config) {
        $scope.vessel = data.vessel;
        Vessel.setVessels(data.vessel);
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
          return "panel-success"
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
        ws.emit("/templog/clear");
    }

    $scope.updateSteps = function(data) {
        $scope.steps = data;
    }

    $scope.setTargetTemp = function(vesselid) {

       //ws.emit("vessel_set_target_temp", {"vesselid": vesselid, "temp":  $scope.new_target_temp[vesselid]});
       //$scope.new_target_temp[vesselid] = undefined;
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

app.run(['Vessel', function(vessel) {
    vessel.init();
}]);
