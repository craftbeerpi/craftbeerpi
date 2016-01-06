var app = angular.module('BrewApp', ['timer', 'ui.bootstrap', 'ngRoute']).config(function($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: 'static/vessel_overview.html',
      name: "Dashboard"
    })
    .when('/chart/:vid', {
      templateUrl: 'static/chart.html'
    })
    .when('/formulas', {
      templateUrl: 'static/volume.html'
    })
    .when('/setup', {
      templateUrl: 'static/setup.html'
    })
    .when('/steps_settings', {
      templateUrl: 'static/steps_settings.html',
      name: "Steps Settings"
    })
    .when('/vessel_settings', {
      templateUrl: 'static/vessel_settings_overview.html',
      name: "Vessel Settings"
    })
    .when('/vessel_settings/id/:vid', {
      templateUrl: 'static/vessel_settings.html'
    })
    .when('/vessel_settings/new', {
      templateUrl: 'static/vessel_settings_new.html'
    })
    .when('/about', {
      templateUrl: 'static/about.html',
      name: "About"
    })
    .when('/volumes/:vid', {
      templateUrl: 'static/volume.html'
    })
    .otherwise({
      redirectTo: '/'
    });
});


app.factory('routeNavigation', function($route, $location) {
  var routes = [];
  angular.forEach($route.routes, function(route, path) {
    if (route.name) {
      routes.push({
        path: path,
        name: route.name
      });
    }
  });
  return {
    routes: routes,
    activeRoute: function(route) {
      return route.path === $location.path();
    }
  };
});

app.factory('Vessel',function($http, ws) {

  var vessel;
  var vessel_temps;
  var vessel_temp_log;
  var steps;

  vessel_update = function(data) {
    console.log("VESSEL UPDATE");
    vessel = data;
  }
  vessel_temp_update = function(data) {
    vessel_temps = data;
  }
  steps_update = function (data) {
    steps = data;
  }

  return {
    init: function() {

      vessel = {}
      $http.get('/vessel/data').
      success(function(data, status, headers, config) {
        console.log(data);
        //vessel = data.vessel;
        vessel_temps = data.vessel_temps;
        vessel_temp_log = data.vessel_temp_log;
      }).
      error(function(data, status, headers, config) {
        // log error
      });

      $http.get('/api/vessel2').
      success(function(data, status, headers, config) {
        console.log(data.objects)
        vessel = data.objects;
      }).
      error(function(data, status, headers, config) {
        // log error
      });


      $http.get('/api/step').
      success(function(data, status, headers, config) {
        console.log(data)
        steps = data.objects;
      }).
      error(function(data, status, headers, config) {
        // log error
      });

      ws.on('vessel_update', vessel_update);
      ws.on('vessel_temp_update', vessel_temp_update);
      ws.on('steps', steps_update);
    },
    vessel: function() {

      return vessel;
    },
    vessel_temps: function() {
      return vessel_temps;
    },
    vessel_temp_log: function() {
      return vessel_temp_log;
    },
    steps: function() {
      return steps;
    }


  };
});


app.directive('navigation', function(routeNavigation) {
  return {
    restrict: "E",
    replace: true,
    templateUrl: "static/navigation-directive.tpl.html",
    controller: function($scope) {
      $scope.routes = routeNavigation.routes;
      $scope.activeRoute = routeNavigation.activeRoute;
    }
  };
});

app.directive('vesselform', function() {
  return {
    restrict: "E",
    replace: true,
    templateUrl: "static/vessel_settings_from.html",
  };
});


app.directive('backButton', function() {
  return {
    restrict: 'A',
    link: function(scope, element, attrs) {
      element.on('click', function() {
        history.back();
        scope.$apply();
      });
    }
  };
});

app.controller('TargetTempCtrl', function($scope, $uibModalInstance, vessel) {

  $scope.target_temp = undefined;
  $scope.vessel = vessel;
  $scope.ok = function() {
    $uibModalInstance.close($scope.target_temp);
  };

  $scope.cancel = function() {
    $uibModalInstance.dismiss('cancel');
  };
});

app.controller('ChartController', function(ws, $scope, $http, Vessel, $routeParams) {

  $scope.load = function() {

    $scope.vessel = Vessel.vessel()[$routeParams.vid];

    $http.get('/vessel/chartdata/' + $routeParams.vid).
    success(function(data, status, headers, config) {
      var chart_data = $scope.downsample(data, "data", "x");
      $scope.chart = c3.generate({
        bindto: '#chart',
        data: {
          xs: {
            data: "x"
          },
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

      });
    }).
    error(function(data, status, headers, config) {
      // log error
    });
  }

  $scope.downsample = function(data, x, y) {
    if (typeof(x) === 'undefined') x = "P1";
    if (typeof(y) === 'undefined') y = "x";

    if (data == undefined) {
      return
    }
    names = [
      [y, x]
    ];
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
});

app.controller('FormularController', function(ws, $scope, $http, $routeParams, Vessel) {

  var v = Vessel.vessel()[$routeParams.vid];
  $scope.vessel_name = v.name;
  $scope.height = v.height;
  $scope.diameter = v.diameter;
  $scope.free = 0;

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
});

app.controller('VesselOverviewController', function(ws, $scope, $http, Vessel, $uibModal) {
  $scope.vessels = Vessel.vessel();
  $scope.vessel_update = function(data) {
    $scope.vessels = data;
  }
  ws.on('vessel_update', $scope.vessel_update);
});


app.controller('VesselController', function(ws, $scope, $http, Vessel, $uibModal, $location, $routeParams) {
  if($routeParams.vid == "new") {
    $scope.vessel = {name: "", sensorid: ""}
  }
  else {
    $scope.vessel = angular.copy(Vessel.vessel()[$routeParams.vid]);
  }
  $scope.options = ["ABC", "DEF"];
  $scope.save = function() {

    if($routeParams.vid == "new") {
      console.log("POST");
      $http.post("/vessel/1", $scope.vessel);
    }
    else {
      Vessel.vessel()[$routeParams.vid] = $scope.vessel;
      $http.put("/vessel/" + $routeParams.vid, $scope.vessel);
    }
    history.back();
  }
  $scope.delete = function() {
    $http.delete("/vessel/" + $routeParams.vid).success(function(data, status, headers, config) {
      $location.url("/vessel_settings");
    });
  }
});

app.controller('NewVesselController', function(ws, $scope, $http, Vessel, $uibModal, $location, $routeParams) {

  $scope.options = ["ABC", "DEF"];
  $scope.save = function() {
      $http.post("/vessel/1", $scope.vessel);
    history.back();
  }
});


app.controller('SetupController', function(ws, $scope, $http, Vessel, $uibModal, $location) {
  $scope.vessel_update = function() {
    $location.url("/vessel_settings");
  }
  ws.on('vessel_update', $scope.vessel_update);

  $scope.setup = function(num) {
    $http.post("/vessel/setup/"+num).success(function(data, status, headers, config) {

    });
  }
});

app.controller('BrewController', function(ws, $scope, $http, Vessel, $uibModal, $location) {
  $scope.vessel = Vessel.vessel();
  $scope.vessel_temps = Vessel.vessel_temps();
  $scope.vessel_temp_log = Vessel.vessel_temp_log();
  $scope.steps = Vessel.steps();

  if($scope.vessel.length == 0) {
    $location.url("/setup");
  }

  // Target Temp Modal Dialog
  $scope.open = function(vid, size) {
    var modalInstance = $uibModal.open({
      animation: true,
      templateUrl: 'static/target_temp.html',
      controller: 'TargetTempCtrl',
      size: size,
      resolve: {
        vessel: function() {
          return $scope.vessel[vid];
        }
      }
    });

    modalInstance.result.then(function(target_temp) {
      if (target_temp != undefined) {
        ws.emit("vessel_set_target_temp", {
          "vesselid": vid,
          "temp": target_temp
        });
      }

    }, function() {
      console.log("dismiss");
    });
  };

  $scope.buttonState = function(state) {
    if (state == true) {
      return "btn-success"
    } else {
      return "btn-default"
    }
  }

  $scope.stepStyle = function(item) {

    var num_of_vessels = Object.keys($scope.vessel_temps).length;

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

  $scope.stateClassIcon = function(item) {
    if (item.state == "A")
      return "fa fa-spinner fa-spin"
    else if (item.state == "D")
      return "fa fa-check";
    else
      return "";
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

  // WebSocket Update methods
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
  ws.on('vessel_update', $scope.vessel_update);
  ws.on('vessel_temp_update', $scope.vessel_temp_update);
  ws.on('vessel_automatic_on', $scope.vessel_automatic_on);
  ws.on('vessel_automatic_off', $scope.vessel_automatic_off);
  ws.on('steps', $scope.updateSteps);
});

// WebSocket Factory
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
      if (data == undefined) {
        socket.emit(event);
      } else {
        socket.emit(event, data);
      }

    }
  }
}]);

app.run(['Vessel', function(vessel) {
  vessel.init();
}]);
