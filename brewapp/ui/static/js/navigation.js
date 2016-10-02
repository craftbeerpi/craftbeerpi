function session () {
    return {}
}

function routes($stateProvider, $urlRouterProvider) {
    //
    // For any unmatched url, redirect to /state1
    $urlRouterProvider.otherwise("/dashboard");
    //
    // Now set up the states
    $stateProvider
        .state('dashboard', {
            url: "/dashboard",
            templateUrl: "/ui/static/partials/dashboard/overview.html"
        })
        .state('about', {
            url: "/about",
            templateUrl: "/ui/static/partials/about/about.html"
        })
        .state('fermentation', {
            url: "/fermentation",
            templateUrl: "/ui/static/partials/fermentation/dashboard.html"
        })
        .state('brewchart', {
            url: "/brewchart/:id",
            templateUrl: "/ui/static/partials/chart/chart.html",
            controller: "ChartController",
            type: "K_",
            back: "dashboard"
        })
        .state('fermentationchart', {
            url: "/fermentationchart/:id",
            templateUrl: "/ui/static/partials/chart/chart.html",
            controller: "ChartController",
            type: "F_",
            back: "fermentation"
        })
        .state('steps', {
            url: "/steps",
            templateUrl: "/ui/static/partials/steps/overview.html"
        })
        .state('config', {
            url: "/config",
            templateUrl: "/ui/static/partials/config/overview.html"
        })
        .state('hardware', {
            url: "/hardware",
            templateUrl: "/ui/static/partials/hardware/overview.html"
        })
        .state('setup', {
            url: "/setup",
            templateUrl: "/ui/static/partials/setup/index.html"
        })
        .state('kbh', {
            url: "/kbh",
            templateUrl: "/ui/static/partials/kbh/overview.html"
        })


}

angular.module("cbpnavigation", []).service("session", session).config(routes);