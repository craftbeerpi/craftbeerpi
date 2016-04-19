angular.module('craftbeerpi.recipebook', [])
.controller('RecipeBook', function($scope, $location, $uibModalInstance, CBPRecipeBook) {

  CBPRecipeBook.query({}, function(response) {
    $scope.items = response.objects;
  });

  $scope.load = function(id) {
    console.log(id);
      CBPRecipeBook.load({"id": id
    }, function(data) {
      $location.url("/step/overview/");
    });
  };

  $scope.delete = function(id) {
    CBPRecipeBook.delete({
      "id": id
    }, function() {
      CBPRecipeBook.query({}, function(response) {
        $scope.items = response.objects;
      });
    });
  };

  $scope.cancel = function() {
    $uibModalInstance.dismiss('cancel');
  };


}).controller('RecipeBookSave',
function($scope, $location,CBPConfig, $uibModalInstance, ConfirmMessage, CBPRecipeBook) {


 $scope.name = $scope.config["BREWNAME"];
  $scope.save = function() {
    $uibModalInstance.close({"name": $scope.name});
  };

  $scope.cancel = function() {
    $uibModalInstance.dismiss('cancel');
  };
});
