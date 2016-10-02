function dummy_controller($scope, $http) {


    $scope.sensors = {}

    $http({
        method: 'GET',
        url: '/api/test/temps'
    }).then(function successCallback(response) {
        $scope.sensors = response.data;
    });

    function post(sliderId, modelValue, highValue, pointerType) {
        $http({
            method: 'POST',
            url: '/set',
            data: {"id": sliderId, "value": modelValue}
        });
    }

    $scope.slider = {
        value: 20,
        options: {
            floor: 0,
            ceil: 101,
            id: "DummySensor1",
            onEnd: post
        },
        getPointerColor: function () {
            return "red";
        }
    };

    $scope.slider2 = {
        value: 20,
        options: {
            floor: 0,
            ceil: 101,
            id: "DummySensor2",
            onEnd: post
        }
    };

    $scope.slider3 = {
        value: 20,
        options: {
            floor: 0,
            ceil: 101,
            id: "DummySensor3",
            onEnd: post
        }
    };
}

function dummytemp() {
    return {
        controller: dummy_controller,

        templateUrl: 'static/partials/test/tempcontrol.html'
    };
}


angular.module("cbpdummytemp", []).directive("dummytemp", dummytemp);