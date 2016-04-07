angular.module('craftberpi.config', []).controller('ConfigOverviewController', function($scope, $location, CBPHardware, ConfirmMessage,  CBPConfig) {
  $scope.configparam = {
    "name": "",
    "value": "",
    "type": "",
  }
  loadAll();
  $scope.save = function() {
    if ($scope.configparam.name.length == 0) {
      return;
    }
    CBPConfig.save($scope.configparam, function(data) {
      loadAll();
    });
  }
  function loadAll() {
    CBPConfig.query({}, function(response) {
        $scope.configparams = response.objects;
    });
  }

}).controller('ConfigEditController', function($scope, $location, $routeParams, CBPHardware, ConfirmMessage, CBPKettle, CBPConfig) {

  $scope.name = $routeParams.id

  CBPConfig.get({
    "name": $scope.name
  }, function(response) {
    $scope.configparam = response;
    console.log($scope.configparam);
  });

  $scope.save = function() {
    CBPConfig.update({
      "name": $scope.configparam.name
    }, $scope.configparam, function() {
      history.back();
    });
  }
  $scope.delete = function() {
    ConfirmMessage.open("Delete Config","Do you really want to delete the parameter?", function() {
      CBPConfig.delete({
        "name": $scope.configparam.name
      }, function() {
        history.back();
      });

    }, function() {

    });
  }
});
