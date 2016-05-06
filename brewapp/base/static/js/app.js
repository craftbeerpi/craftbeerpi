angular.module('craftberpi',
['mgo-angular-wizard',
'timer','angularFileUpload',
'ngResource', 'ui.bootstrap',
'ngRoute',
'easypiechart',
'craftberpi.controllers',
'craftbeerpi.kettle',
'craftberpi.controllers2',
'craftberpi.controllers3',
'craftberpi.controllers6',
'craftbeerpi.recipebook',
'craftbeerpi.hardware',
'craftbeerpi.services',
'craftbeerpi.about',
'pascalprecht.translate',
'ngCookies',
'craftberpi.config']).config(function($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: '/base/static/partials/dashboard/overview.html',
      name: "Dashboard"
    })
    .when('/step/overview', {
      templateUrl: '/base/static/partials/steps/overview.html',
      name: "Steps"
    })
    .when('/setup', {
      templateUrl: '/base/static/partials/setup/setup.html',
    })
    .when('/kettle/overview', {
      templateUrl: '/base/static/partials/kettle/overview.html',
      name: "Kettle"
    })
    .when('/pump/overview', {
      templateUrl: '/base/static/partials/hardware/overview.html',
      name: "Additional Hardware"
    })
    .when('/pump/:vid', {
      templateUrl: '/base/static/partials/hardware/edit.html',
    })
    .when('/config', {
      templateUrl: '/base/static/partials/config/overview.html',
      name: "Configuration"
    })
    .when('/config/:id', {
      templateUrl: '/base/static/partials/config/edit.html',
    })
    .when('/about', {
      templateUrl: '/base/static/partials/about/about.html',
      name: "About"
    })
    .when('/kettle/:vid', {
      templateUrl: '/base/static/partials/kettle/edit.html',
      controller: 'KettleEditController',
    })
    .when('/chart/:vid', {
      templateUrl: '/base/static/partials/chart/chart.html',
    })
    .when('/step/kb', {
      templateUrl: '/base/static/partials/steps/kbupload.html',
    })
    .when('/step/recipe_book', {
      templateUrl: '/base/static/partials/steps/recipe_book_overview.html',
    })
    .when('/step/:vid', {
      templateUrl: '/base/static/partials/steps/edit.html',
    })
    .otherwise({
      redirectTo: '/'
    });
}).config(['$translateProvider', function ($translateProvider) {
  // configures staticFilesLoader
  $translateProvider.useStaticFilesLoader({
    prefix: '/static/languages/',
    suffix: '.json'
  }).fallbackLanguage('en');
  $translateProvider.useCookieStorage();
  $translateProvider.determinePreferredLanguage()
}]);
