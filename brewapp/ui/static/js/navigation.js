function session () {
    return {}
}

function routes($stateProvider, $urlRouterProvider) {
    //
    // For any unmatched url, redirect to /state1
    $urlRouterProvider.otherwise("/start");
    //
    // Now set up the states
    $stateProvider
        .state('start', {
            url: "/start",
            controller: function (CBPConfig, $state) {
                CBPConfig.setup(function (data) {
                    console.log(data.setup)
                    if(data.setup == "Yes") {
                        $state.go("setup")
                    }
                    else {
                        $state.go("dashboard")
                    }

                })
            }
        })
        .state('setup', {
            url: "/setup",
            templateUrl: "/ui/static/partials/setup/index.html"
        })
        .state('main', {
            templateUrl: "/ui/static/main.html"
        })
        .state('dashboard', {
            url: "/dashboard",
            templateUrl: "/ui/static/partials/dashboard/overview.html",
            parent: 'main'
        })
        .state('about', {
            url: "/about",
            templateUrl: "/ui/static/partials/about/about.html",
            parent: 'main'
        })
        .state('dummy', {
            url: "/dummy",
            templateUrl: "/ui/static/partials/dummy.html",

        })
        .state('fermentation', {
            url: "/fermentation",
            templateUrl: "/ui/static/partials/fermentation/dashboard.html",
            parent: 'main'
        })
        .state('brewchart', {
            url: "/brewchart/:id",
            templateUrl: "/ui/static/partials/chart/chart.html",
            controller: "ChartController",
            type: "K",
            title: "KETTLE_CHART",
            back: "dashboard",
            parent: 'main'
        })
        .state('fermentationchart', {
            url: "/fermentationchart/:id",
            templateUrl: "/ui/static/partials/chart/chart.html",
            controller: "ChartController",
            type: "F",
            title: "FERMENTER",
            back: "fermentation",
            parent: 'main'
        })
        .state('steps', {
            url: "/steps",
            templateUrl: "/ui/static/partials/steps/overview.html",
            parent: 'main'
        })
        .state('config', {
            url: "/config",
            templateUrl: "/ui/static/partials/config/overview.html",
            parent: 'main'
        })
        .state('hardware', {
            url: "/hardware",
            templateUrl: "/ui/static/partials/hardware/overview.html",
            parent: 'main'
        })
        .state('beerxml', {
            url: "/beerxml",
            templateUrl: "/ui/static/partials/beerxml/overview.html",
            parent: 'main'
        })
        .state('kbh', {
            url: "/kbh",
            templateUrl: "/ui/static/partials/kbh/overview.html",
            parent: 'main'
        })


}

angular.module("cbpnavigation", []).service("session", session).config(routes);