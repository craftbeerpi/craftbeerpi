var app = angular.module('BrewApp', ['timer', 'ui.bootstrap', 'ngRoute']).config(function($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: 'static/kettle_overview.html',
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
    .when('/kettle_settings', {
      templateUrl: 'static/kettle_settings_overview.html',
      name: "Kettle Settings"
    })
    .when('/kettle_settings/id/:vid', {
      templateUrl: 'static/kettle_settings.html'
    })
    .when('/kettle_settings/new', {
      templateUrl: 'static/kettle_settings_new.html'
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

app.factory('Kettle',function($http, ws) {

  var kettle;
  var kettle_temps;
  var kettle_temp_log;
  var steps;

  kettle_update = function(data) {
    console.log("VESSEL UPDATE");
    kettle = data;
  }
  kettle_temp_update = function(data) {
    kettle_temps = data;
  }
  steps_update = function (data) {
    steps = data;
  }

  return {
    init: function() {

      kettle = {}
      $http.get('/kettle/data').
      success(function(data, status, headers, config) {
        console.log(data);
        //kettle = data.kettle;
        kettle_temps = data.kettle_temps;
        kettle_temp_log = data.kettle_temp_log;
      }).
      error(function(data, status, headers, config) {
        // log error
      });

      $http.get('/api/kettle2').
      success(function(data, status, headers, config) {
        console.log(data.objects)
        kettle = data.objects;
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

      ws.on('kettle_update', kettle_update);
      ws.on('kettle_temp_update', kettle_temp_update);
      ws.on('steps', steps_update);
    },
    kettle: function() {

      return kettle;
    },
    kettle_temps: function() {
      return kettle_temps;
    },
    kettle_temp_log: function() {
      return kettle_temp_log;
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

app.directive('kettleform', function() {
  return {
    restrict: "E",
    replace: true,
    templateUrl: "static/kettle_settings_from.html",
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

app.controller('TargetTempCtrl', function($scope, $uibModalInstance, kettle) {

  $scope.target_temp = undefined;
  $scope.kettle = kettle;
  $scope.ok = function() {
    $uibModalInstance.close($scope.target_temp);
  };

  $scope.cancel = function() {
    $uibModalInstance.dismiss('cancel');
  };
});

app.controller('ChartController', function(ws, $scope, $http, Kettle, $routeParams) {

  $scope.load = function() {

    $scope.kettle = Kettle.kettle()[$routeParams.vid];

    $http.get('/kettle/chartdata/' + $routeParams.vid).
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

app.controller('FormularController', function(ws, $scope, $http, $routeParams, Kettle) {

  var v = Kettle.kettle()[$routeParams.vid];
  $scope.kettle_name = v.name;
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

app.controller('KettleOverviewController', function(ws, $scope, $http, Kettle, $uibModal) {
  $scope.kettles = Kettle.kettle();
  $scope.kettle_update = function(data) {
    $scope.kettles = data;
  }
  ws.on('kettle_update', $scope.kettle_update);
});


app.controller('KettleController', function(ws, $scope, $http, Kettle, $uibModal, $location, $routeParams) {
  if($routeParams.vid == "new") {
    $scope.kettle = {name: "", sensorid: ""}
  }
  else {
    $scope.kettle = angular.copy(Kettle.kettle()[$routeParams.vid]);
  }
  $scope.options = ["ABC", "DEF"];
  $scope.save = function() {

    if($routeParams.vid == "new") {
      console.log("POST");
      $http.post("/kettle/1", $scope.kettle);
    }
    else {
      Kettle.kettle()[$routeParams.vid] = $scope.kettle;
      $http.put("/kettle/" + $routeParams.vid, $scope.kettle);
    }
    history.back();
  }
  $scope.delete = function() {
    $http.delete("/kettle/" + $routeParams.vid).success(function(data, status, headers, config) {
      $location.url("/kettle_settings");
    });
  }
});

app.controller('NewKettleController', function(ws, $scope, $http, Kettle, $uibModal, $location, $routeParams) {

  $scope.options = ["ABC", "DEF"];
  $scope.save = function() {
      $http.post("/kettle/1", $scope.kettle);
    history.back();
  }
});


app.controller('SetupController', function(ws, $scope, $http, Kettle, $uibModal, $location) {
  $scope.kettle_update = function() {
    $location.url("/kettle_settings");
  }
  ws.on('kettle_update', $scope.kettle_update);

  $scope.setup = function(num) {
    $http.post("/kettle/setup/"+num).success(function(data, status, headers, config) {

    });
  }
});

app.controller('BrewController', function(ws, $scope, $http, Kettle, $uibModal, $location) {
  $scope.kettle = Kettle.kettle();
  $scope.kettle_temps = Kettle.kettle_temps();
  $scope.kettle_temp_log = Kettle.kettle_temp_log();
  $scope.steps = Kettle.steps();

  if($scope.kettle.length == 0) {
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
        kettle: function() {
          return $scope.kettle[vid];
        }
      }
    });

    modalInstance.result.then(function(target_temp) {
      if (target_temp != undefined) {
        ws.emit("kettle_set_target_temp", {
          "kettleid": vid,
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

    var num_of_kettles = Object.keys($scope.kettle_temps).length;

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

  $scope.stateClassIcon = function(item) {
    if (item.state == "A")
      return "fa fa-spinner fa-spin"
    else if (item.state == "D")
      return "fa fa-check";
    else
      return "";
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

  // WebSocket Update methods
  $scope.kettle_update = function(data) {
    $scope.kettle = data;
  }
  $scope.kettle_temp_update = function(data) {
    $scope.kettle_temps = data;
  }
  $scope.kettle_automatic_on = function(data) {
    $scope.kettle[data].heater.state = true;
  }
  $scope.kettle_automatic_off = function(data) {
    $scope.kettle[data].heater.state = false;
  }
  $scope.kettle_gpio = function(gpio) {
    ws.emit("kettle_gpio", gpio)
  }
  $scope.kettle_automatic = function(kettleid) {
    ws.emit("kettle_automatic", kettleid)
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
  ws.on('kettle_update', $scope.kettle_update);
  ws.on('kettle_temp_update', $scope.kettle_temp_update);
  ws.on('kettle_automatic_on', $scope.kettle_automatic_on);
  ws.on('kettle_automatic_off', $scope.kettle_automatic_off);
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

app.run(['Kettle', function(kettle) {
  kettle.init();
}]);
