function CBPSteps($resource) {
    return $resource("/api/step/:id", {}, {
        query: {
            method: 'GET',
            isArray: false
        },
        update: {
            method: 'PUT'
        },
        clear: {
            method: 'POST',
            url: '/api/step/clear',
            isArray: false
        },
        order: {
            method: 'POST',
            url: '/api/step/order',
            isArray: false
        }
    });
}


function CBPKettle($resource) {
    return $resource("/api/kettle/:id", {}, {
        query: {
            method: 'GET',
            isArray: false
        },
        update: {
            method: 'PUT'
        },
        getstate: {
            method: 'GET',
            url: '/api/kettle/state',
            isArray: false
        },
        getthermometer: {
            method: 'GET',
            url: '/api/thermometer/sensors',
            isArray: true
        },
        getDevices: {
            method: 'GET',
            url: '/api/hardware/devices',
            isArray: true
        },
        automatic: {
            method: 'POST',
            url: '/api/kettle/:id/automatic',
            params: {id: '@id'},
            isArray: false
        },
        targettemp: {
            method: 'POST',
            url: '/api/kettle/:id/targettemp',
            params: {id: '@id'},
            isArray: false
        },
        getchart: {
            method: 'GET',
            url: '/api/kettle/chart/:id',
            isArray: false
        },
        getautomatic: {
            method: 'GET',
            url: '/api/automatic/paramter',
            isArray: true
        },
        clear: {
            method: 'POST',
            url: '/api/thermometer/clear',
            isArray: false
        },
        getLastTemp: {
            method: 'GET',
            url: '/api/thermometer/last',
            isArray: false
        },
        getTemps: {
            method: 'GET',
            url: '/api/thermometer/kettle/:id',
            isArray: false
        }
    });
}


function CBPSwitch($http) {
    return {
        get: function (okCallback) {
            $http({
                method: 'GET',
                url: '/api/switch'
            }).then(function successCallback(response) {
                okCallback(response.data);
            }, function errorCallback(response) {

            });
        }
    }
};

function CBPHardware($resource) {
    return $resource("/api/hardware/:id", {}, {
        query: {
            method: 'GET',
            isArray: false
        },
        update: {
            method: 'PUT'
        },
        getstate: {
            method: 'GET',
            url: '/api/hardware/state',
            isArray: false
        }
    });
}


function CBPConfig($resource) {
    return $resource("/api/config/:name", {}, {
        query: {
            method: 'GET',
            isArray: false
        },
        update: {
            method: 'PUT'
        }
    });
}


function Braufhelfer($http) {
    return {

        get: function (okCallback) {
            $http({
                method: 'GET',
                url: '/base/kb'
            }).then(function successCallback(response) {
                okCallback(response.data);
            }, function errorCallback(response) {

            });
        },

        load: function (id, d, okCallback) {
            $http({
                method: 'POST',
                data: d,
                url: '/base/kb/select/' + id
            }).then(function successCallback(response) {
                okCallback(response.data);
            }, function errorCallback(response) {

            });
        }
    }
}

function CBPRecipeBook($resource) {
    return $resource("/api/recipe_books/:id", {}, {
        query: {
            method: 'GET',
            isArray: false
        },
        update: {
            method: 'PUT'
        },
        load: {
            method: 'POST',
            params: {id: '@id'},
            url: '/api/recipe_books/load/:id',
            isArray: false
        },
        save: {
            method: 'POST',
            url: '/api/recipe_books/save',

            isArray: false
        }
    });
}

function CBPSetup($resource) {
    return $resource("/api/setup/kettle", {}, {
        setup: {
            url: '/api/setup/kettle',
            method: 'POST',
            isArray: false
        },
        hardware: {
            url: '/api/setup/hardware',
            method: 'POST',
            isArray: true
        },
        thermometer: {
            url: '/api/setup/thermometer',
            method: 'POST',
            isArray: true
        }

    });
}

function helloWorld() {

}

angular.module("cbpresource", [])
    .factory("CBPKettle", CBPKettle)
    .factory("CBPSetup", CBPSetup)
    .factory("CBPSwitch", CBPSwitch)
    .factory("CBPSteps", CBPSteps)
    .factory("CBPConfig", CBPConfig)
    .factory("Braufhelfer", Braufhelfer)
    .factory("CBPRecipeBook", CBPRecipeBook)
    .service("helloWorld", helloWorld)
    .factory("CBPHardware", CBPHardware);
