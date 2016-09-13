function navigation(routeNavigation) {
    return {
        restrict: "E",
        replace: true,
        templateUrl: "static/partials/navigation.html",
        controller: function ($scope) {
            $scope.routes = routeNavigation.routes;
            $scope.activeRoute = routeNavigation.activeRoute;
        }
    };
};

function routeNavigation($route, $location) {
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
        //routes: routes,
        routes: routes,
        activeRoute: function (route) {
            return route.path === $location.path();
        }
    };
}


function navigationConfig($routeProvider) {
    $routeProvider
        .when('/dashboard', {
            templateUrl: '/ui/static/partials/dashboard/overview.html',
            name: "BREWING"
        })
        .when('/fermentation', {
            templateUrl: '/ui/static/partials/fermentation/dashboard.html',
            name: "FERMENTATION"
        })
        .when('/kettle', {
            templateUrl: '/ui/static/partials/kettle/overview.html',
            controller: 'kettleOverviewController',
            name: "KETTLE"
        })
        .when('/test', {
            templateUrl: '/ui/static/partials/kbh/overview.html'
        })
        .when('/chart/:id', {
            templateUrl: '/ui/static/partials/chart/chart.html',
        })
        .when('/steps', {
            templateUrl: '/ui/static/partials/steps/overview.html',
            name: "STEPS"
        })
        .when('/hardware', {
            templateUrl: '/ui/static/partials/hardware/overview.html',
            name: "HARDWARE"
        })
        .when('/config', {
            templateUrl: '/ui/static/partials/config/overview.html',
            name: "CONFIGURATION"
        })
        .when('/about', {
            templateUrl: '/ui/static/partials/about/about.html',
            name: "ABOUT"
        })
        .when('/fermentation/chart/:id', {
            templateUrl: '/ui/static/partials/fermentation/chart.html',
        })

        .otherwise({
            redirectTo: '/dashboard'
        });
}

angular.module("cbpnavigation", [])
    .directive("navigation", navigation)
    .factory("routeNavigation", routeNavigation)
    .config(navigationConfig)
