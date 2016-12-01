angular.module("test",
    ['timer',
        'ui.router',
        'btford.socket-io',
        'angularFileUpload',
        'pascalprecht.translate',
        'ngCookies',
        'cbpnavigation',
        'cbpwebsocket',
        'cbpresource',
        'cbpfilter',
        'ui.tree',
        'ui.bootstrap',
        'mgo-angular-wizard',
        'cbpdummytemp',
        'ngResource', 'rzModule',

        'cbpcontroller'])
    .config(['$translateProvider', function ($translateProvider) {
        $translateProvider.useStaticFilesLoader({
            prefix: 'static/languages/',
            suffix: '.json'
        }).fallbackLanguage('en');
        $translateProvider.preferredLanguage('en');
        $translateProvider.useCookieStorage();
        //$translateProvider.determinePreferredLanguage()



    }]).run(function ($rootScope, CBPConfig, ConfirmMessage) {

        $rootScope.config = {};

        $rootScope.inArray = function (item, array) {
            return (-1 !== array.indexOf(item));
        };
    
        CBPConfig.query(function (data) {

        data.objects.forEach(function (entry) {
            $rootScope.config[entry.name] = entry.value
        });

        $rootScope.$on('socket:config', function (ev, data) {
            $rootScope.config = data;
        });
        $rootScope.$on('socket:message', function (ev, data) {
            console.log("MESSAGE")
            ConfirmMessage.open(data.headline, data.message, function () {
        });
    });

    });


});