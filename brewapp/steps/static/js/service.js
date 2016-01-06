angular.module('myApp.services', []).factory("MyBucket", function($resource) {
  return $resource("/api/step/:id", {}, {
    query: {
      method: 'GET',
      isArray: false
    },
    update: {
      method: 'PUT'
    },
    markAllComplete: {
      method: 'PUT',
      params: {
        complete: true
      },
      isArray: true
    }
  });
}).factory('routeNavigation', function($route, $location) {
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
    templateUrl: "/steps/static/partials/navigation.html",
    controller: function($scope) {
      $scope.routes = routeNavigation.routes;
      $scope.activeRoute = routeNavigation.activeRoute;
    }
  };
});
