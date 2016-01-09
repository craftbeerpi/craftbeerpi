angular.module('myApp.services', []).factory("CBPSteps", function($resource) {
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
  return $resource("/api/kettle2/:id", {}, {
    query: {
      method: 'GET',
      isArray: false
    },
    update: {
      method: 'PUT'
    },
    getstate: {
      method: 'GET',
      url: '/api/kettle2/state',
      isArray: false
    },
    getthermometer: {
      method: 'GET',
      url: '/api/kettle2/thermometer',
      isArray: true
    },
    getchart: {
      method: 'GET',
      url: '/api/kettle2/chart/:id',
      isArray: true
    },
    clear: {
      method: 'POST',
      url: '/api/kettle2/clear',
      isArray: false
    }
  });
}).factory("Braufhelfer", function($http) {
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
        url: '/base/kb/select/'+id
      }).then(function successCallback(response) {
        okCallback(response.data);
      }, function errorCallback(response) {

      });
    }
  }

}).factory('ws', ['$rootScope', function($rootScope) {
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
});
