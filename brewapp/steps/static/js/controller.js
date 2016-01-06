angular.module('myApp.controllers', []).controller('MyController', function($scope, $location, MyBucket, $injector) {

  console.log($injector.has('navigation'));

  MyBucket.query({}, function(response) {
    $scope.hosts = response.objects
  });
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
    MyBucket.save($scope.step, function(data) {
      console.log("reload");
      MyBucket.query({}, function(response) {
        $scope.hosts = response.objects;
      });
    });
  }

}).controller('EditStep', function($scope, MyBucket, $routeParams) {
  // Do something with myService
  $scope.vid = $routeParams.vid
  $scope.type = [{
    "key": "A",
    "value": "Automatic"
  }, {
    "key": "M",
    "value": "Manuell"
  }]
  MyBucket.query({}, function(response) {
    $scope.hosts = response.objects;
    MyBucket.get({
      "id": $scope.vid
    }, function(response) {
      $scope.step = response;
    });
    $scope.save = function() {

      MyBucket.update({
        "id": $scope.step.id
      }, $scope.step);
    }
    $scope.delete = function() {
      MyBucket.delete({
        "id": $scope.step.id
      }, function() {
        history.back();
      });
    }
  });
}).controller('NewStep', function($scope, MyBucket, $routeParams, $location) {
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
    MyBucket.save($scope.step, function(data) {

      $location.url("/step/" + data.id);

    });
  }
  $scope.savenext = function() {
    console.log($scope.step);
    MyBucket.save($scope.step, function(data) {
      $scope.step = {}
      $location.url("/new/");

    });
  }

});
