angular.module('craftberpi.config', []).controller('ConfigOverviewController', function($uibModal, $scope, $location, CBPHardware, ConfirmMessage,  CBPConfig) {

  loadAll();

  function loadAll() {
    CBPConfig.query({}, function(response) {
        $scope.configparams = response.objects;
  });
  }

  $scope.edit = function(id) {
    $scope.selected = id
    var modalInstance = $uibModal.open({
      animation: true,
      controller: "ConfigEditController",
      scope: $scope,
      templateUrl: '/base/static/partials/config/form.html',
      size: "sm",
      //resolve: {"id": id}
    });
    modalInstance.result.then(function(data) {
      loadAll()
    });
  }

}).controller('ConfigEditController', function($scope,$uibModalInstance, CBPConfig) {

  $scope.name = $scope.selected;

  CBPConfig.get({
    "name": $scope.name
  }, function(response) {
    $scope.configparam = response;

    if($scope.configparam.options != null) {
      $scope.options = $scope.configparam.options.split(',');
    }

  });

  $scope.save = function() {
    CBPConfig.update({
      "name": $scope.configparam.name
    }, $scope.configparam, function() {
      $uibModalInstance.close({});
    });
  }
  $scope.cancel = function() {
    $uibModalInstance.dismiss('cancel');
  };
});
