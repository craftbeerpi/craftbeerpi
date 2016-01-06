angular.module('myApp', ['ngResource', 'ngRoute', 'myApp.controllers', 'myApp.services', 'ui.sortable', 'dndLists']).config(function($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: '/steps/static/partials/steps/overview.html',
      name: "Main"
    })
    .when('/new/', {
      templateUrl: '/steps/static/partials/steps/new.html',
      name: "New"
    })
    .when('/step/:vid', {
      templateUrl: '/steps/static/partials/steps/edit.html',
    })
    .otherwise({
      redirectTo: '/'
    });
});
