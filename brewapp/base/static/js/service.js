angular.module('craftbeerpi.services', []).factory("CBPSteps", function($resource) {
  return $resource("/api/step/:id", {}, {
    query: {
      method: 'GET',
      isArray: false
    },
    update: {
      method: 'PUT'
    },
    clear: {
      method: 'POST',
      url: '/api/step/clear',
      isArray: false
    }

  });
}).
factory("CBPKettle", function($resource) {
  return $resource("/api/kettle/:id", {}, {
    query: {
      method: 'GET',
      isArray: false
    },
    update: {
      method: 'PUT'
    },
    getstate: {
      method: 'GET',
      url: '/api/kettle/state',
      isArray: false
    },
    getthermometer: {
      method: 'GET',
      url: '/api/kettle/thermometer',
      isArray: true
    },
    getDevices: {
      method: 'GET',
      url: '/api/kettle/devices',
      isArray: true
    },
    getchart: {
      method: 'GET',
      url: '/api/kettle/chart/:id',
      isArray: false
    },
    getautomatic: {
      method: 'GET',
      url: '/api/automatic/paramter',
      isArray: true
    },
    clear: {
      method: 'POST',
      url: '/api/kettle/clear',
      isArray: false
    }
  });
}).
factory("CBPHardware", function($resource) {
  return $resource("/api/hardware/:id", {}, {
    query: {
      method: 'GET',
      isArray: false
    },
    update: {
      method: 'PUT'
    },
    getstate: {
      method: 'GET',
      url: '/api/hardware/state',
      isArray: false
    }
  });
}).
factory("CBPRecipeBook", function($resource) {
  return $resource("/api/recipe_books/:id", {}, {
    query: {
      method: 'GET',
      isArray: false
    },
    update: {
      method: 'PUT'
    },
    load: {
      method: 'POST',
      params: {id: '@id'},
      url: '/api/recipe_books/load/:id',
      isArray: false
    },
    save: {
      method: 'POST',
      url: '/api/recipe_books/save',

      isArray: false
    }
  });
})
.factory("CBPConfig", function($resource) {
  return $resource("/api/config/:name", {}, {
    query: {
      method: 'GET',
      isArray: false
    },
    update: {
      method: 'PUT'
    }
  });
})
.factory("Braufhelfer", function($http) {
  return {

    get: function(okCallback) {
      $http({
        method: 'GET',
        url: '/base/kb'
      }).then(function successCallback(response) {
        okCallback(response.data);
      }, function errorCallback(response) {

      });
    },

    load: function(id, d, okCallback) {
      $http({
        method: 'POST',
        data: d,
        url: '/base/kb/select/' + id
      }).then(function successCallback(response) {
        okCallback(response.data);
      }, function errorCallback(response) {

      });
    }
  }
})
.factory("CBPSwitch", function($http) {
  return {
    get: function(okCallback) {
      $http({
        method: 'GET',
        url: '/api/switch'
      }).then(function successCallback(response) {
        okCallback(response.data);
      }, function errorCallback(response) {

      });
    }
  }
})
.factory('ws', ['$rootScope', function($rootScope) {
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
}]).
factory('routeNavigation', function($route, $location) {
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
    //routes: routes,
    routes: routes,
    activeRoute: function(route) {
      return route.path === $location.path();
    }
  };
}).directive('backButton', function() {
  return {
    restrict: 'A',
    link: function(scope, element, attrs) {
      element.on('click', function() {
        history.back();
        scope.$apply();
      });
    }
  };
}).
factory('ChartFactory', function($route, $location) {

  var charts = {};

  return {
    add: function(id, c) {

      charts[id] = c;
    },
    get: function() {
      return charts;
    }
  }

}).directive('chart', function(ChartFactory) {
  return {
    restrict: 'E',
    template: "<div></div>",
    scope: {
      kettle: "=kettle"
    },
    link: function(scope, element, attrs) {
      console.log(scope.kettle)
      var chart = c3.generate({
        bindto: element.context,
        data: {
          columns: [
            ['data1', 30, 200, 100, 400, 150, 250]
          ],
          type: 'area-spline',
        },
        size: {
          height: 150
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
      });
      ChartFactory.add(scope.kettle.id, chart);
    },

  };
}).directive('navigation', function(routeNavigation) {
  return {
    restrict: "E",
    replace: true,
    templateUrl: "/base/static/partials/navigation.html",
    controller: function($scope) {
      $scope.routes = routeNavigation.routes;
      $scope.activeRoute = routeNavigation.activeRoute;
    }
  };
})
.factory('ConfirmMessage', function($route, $location, $uibModal) {

    return {
      open: function(headline, message, confirm, cancel) {

        var modalInstance = $uibModal.open({
          animation: true,
          templateUrl: '/base/static/partials/common/confirm.html',
          controller: 'ConfirmController',
          size: "sm",
          resolve: {
            headline: function() {
              return headline
            },
            message: function() {
              return message
            }
          }
        });
        modalInstance.result.then(function(data) {
          confirm()
        }, function() {
          cancel()
        })
      }
    }
  })
  .controller('ConfirmController', function($scope, $uibModalInstance, headline, message) {
    $scope.message = message;
    $scope.headline = headline;
    $scope.ok = function() {
      $uibModalInstance.close();
    };

    $scope.cancel = function() {
      $uibModalInstance.dismiss('cancel');
    };
  }).
  factory('InfoMessage', function($route, $location, $uibModal) {

      return {
        open: function(headline, message, confirm, cancel) {

          var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: '/base/static/partials/common/info.html',
            controller: 'InfoController',
            size: "sm",
            resolve: {
              headline: function() {
                return headline
              },
              message: function() {
                return message
              }
            }
          });
          modalInstance.result.then(function(data) {
            confirm()
          }, function() {
            cancel()
          })
        }
      }
    })
    .controller('InfoController', function($scope, $uibModalInstance, headline, message) {
      $scope.message = message;
      $scope.headline = headline;
      $scope.ok = function() {
        $uibModalInstance.close();
      };

      $scope.cancel = function() {
        $uibModalInstance.dismiss('cancel');
      };
    }) ;
