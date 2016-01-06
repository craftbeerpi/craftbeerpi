angular.module('myApp.controllers', []).controller('StepOverviewController', function($scope, $location, CBPSteps,CBPVessel) {


  $scope.vessels = [];
  $scope.vessels.push({"key":0, "value":"No Vessel"})
  CBPSteps.query({}, function(response) {
    $scope.steps = response.objects
  });

  CBPVessel.query({}, function(response) {
    angular.forEach(response.objects, function(d) {
        $scope.vessels.push({"key":d.id, "value":d.name});
    })
  });


  $scope.getVesselName = function(vid) {
    if($scope.vessels == undefined) {
      return
    }
    for(i = 0; i < $scope.vessels.length; i++) {
      if(vid == $scope.vessels[i]["key"]) {
        return $scope.vessels[i]["value"];
      }
    }
  }

  $scope.step = {
    "type": "A",
    "state": "I",
    "vesselid": 0
  }

  $scope.type = [{
    "key": "A",
    "value": "Automatic"
  }, {
    "key": "M",
    "value": "Manuell"
  }]

  $scope.save = function() {
    if($scope.step.name == undefined && $scope.step.name.length == 0) {
      return;
    }
    CBPSteps.save($scope.step, function(data) {
      CBPSteps.query({}, function(response) {
        $scope.steps = response.objects;
      });
    });
  }

}).controller('EditStep', function($scope, CBPSteps, CBPVessel, $routeParams) {
  // Do something with myService
  $scope.vid = $routeParams.vid
  $scope.type = [{
    "key": "A",
    "value": "Automatic"
  }, {
    "key": "M",
    "value": "Manuell"
  }]

  $scope.vessels = [];
  $scope.vessels.push({"key":0, "value":"No Vessel"})
  CBPVessel.query({}, function(response) {
    angular.forEach(response.objects, function(d) {
        $scope.vessels.push({"key":d.id, "value":d.name});
    })
  });

  CBPSteps.query({}, function(response) {
    $scope.hosts = response.objects;
    CBPSteps.get({
      "id": $scope.vid
    }, function(response) {
      $scope.step = response;
    });
    $scope.save = function() {

      CBPSteps.update({
        "id": $scope.step.id
      }, $scope.step, function() {
        history.back();
      });
    }
    $scope.delete = function() {
      CBPSteps.delete({
        "id": $scope.step.id
      }, function() {
        history.back();
      });
    }
  });
}).controller('NewStep', function($scope, CBPSteps, $routeParams, $location) {
  // Do something with myService


  $scope.step = {
    "type": "A"
  }
  $scope.type = [{
    "key": "A",
    "value": "Automatic"
  }, {
    "key": "M",
    "value": "Manuell"
  }]

  $scope.save = function() {
    console.log($scope.step);
    CBPSteps.save($scope.step, function(data) {

      $location.url("/step/" + data.id);

    });
  }
  $scope.savenext = function() {
    console.log($scope.step);
    CBPSteps.save($scope.step, function(data) {
      $scope.step = {}
      $location.url("/new/");

    });
  }

});
