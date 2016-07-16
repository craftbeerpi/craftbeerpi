angular.module("test",
    ['ngRoute', 'timer',
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
        'ngResource', 'rzModule',
        'cbpcontroller'])
    .config(['$translateProvider', function ($translateProvider) {


        $translateProvider.useStaticFilesLoader({
            prefix: 'static/languages/',
            suffix: '.json'
        }).fallbackLanguage('en');

        $translateProvider.useCookieStorage();
        $translateProvider.determinePreferredLanguage()
    }]);