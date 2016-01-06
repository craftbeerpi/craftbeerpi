angular.module('myApp', ['ngResource', 'ui.bootstrap', 'ngRoute', 'myApp.controllers', 'myApp.controllers5','myApp.controllers2', 'myApp.controllers3','myApp.services', 'ui.sortable', 'dndLists']).config(function($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: '/base/static/partials/dashboard/overview.html',
      name: "Dashboard"
    })
    .when('/step/overview', {
      templateUrl: '/base/static/partials/steps/overview.html',
      name: "Steps"
    })

    .when('/vessel/overview', {
      templateUrl: '/base/static/partials/vessel/overview.html',
      name: "Vessel"
    })
    .when('/about', {
      templateUrl: '/base/static/partials/about/about.html',
      name: "About"
    })
    .when('/vessel/:vid', {
      templateUrl: '/base/static/partials/vessel/edit.html',
    })
    .when('/chart/:vid', {
      templateUrl: '/base/static/partials/chart/chart.html',
    })
    .when('/step/:vid', {
      templateUrl: '/base/static/partials/steps/edit.html',
    })
    .otherwise({
      redirectTo: '/'
    });
});
