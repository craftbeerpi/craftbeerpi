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
        'cbpdummytemp',
        'ngResource', 'rzModule',
        'cbpcontroller'])
    .config(['$translateProvider', function ($translateProvider) {


        $translateProvider.useStaticFilesLoader({
            prefix: 'static/languages/',
            suffix: '.json'
        }).fallbackLanguage('en_US');
        $translateProvider.preferredLanguage('en_US');
        $translateProvider.useCookieStorage();
        $translateProvider.determinePreferredLanguage()
    }]);