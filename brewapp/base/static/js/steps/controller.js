angular.module('myApp.controllers', []).controller('StepOverviewController', function($scope, $location, CBPSteps,CBPKettle) {


  $scope.kettles = [];
  $scope.kettles.push({"key":0, "value":"No Kettle"})
  CBPSteps.query({}, function(response) {
    $scope.steps = response.objects
  });

  CBPKettle.query({}, function(response) {
    angular.forEach(response.objects, function(d) {
        $scope.kettles.push({"key":d.id, "value":d.name});
    })
  });


  $scope.getKettleName = function(vid) {
    if($scope.kettles == undefined) {
      return
    }
    for(i = 0; i < $scope.kettles.length; i++) {
      if(vid == $scope.kettles[i]["key"]) {
        return $scope.kettles[i]["value"];
      }
    }
  }

  $scope.step = {
    "type": "A",
    "state": "I",
    "kettleid": 0
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

}).controller('EditStep', function($scope, CBPSteps, CBPKettle, $routeParams) {
  // Do something with myService
  $scope.vid = $routeParams.vid
  $scope.type = [{
    "key": "A",
    "value": "Automatic"
  }, {
    "key": "M",
    "value": "Manuell"
  }]

  $scope.kettles = [];
  $scope.kettles.push({"key":0, "value":"No Kettle"})
  CBPKettle.query({}, function(response) {
    angular.forEach(response.objects, function(d) {
        $scope.kettles.push({"key":d.id, "value":d.name});
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
