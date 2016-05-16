angular.module('craftberpi.controllers', []).controller('StepOverviewController', function($scope, $location, CBPSteps, CBPKettle, CBPConfig, CBPRecipeBook, FileUploader, $uibModal, ConfirmMessage) {

  $scope.kettles = [];
  $scope.kettles.push({
    "key": 0,
    "value": "No Kettle"
  })
  $scope.config = {}
  CBPSteps.query({}, function(response) {
    $scope.steps = response.objects
  });

  CBPKettle.query({}, function(response) {
    angular.forEach(response.objects, function(d) {
      $scope.kettles.push({
        "key": d.id,
        "value": d.name
      });
    })
  });

  CBPConfig.query(function(data) {
    data.objects.forEach(function(entry) {
      $scope.config[entry.name] = entry.value
    });
  });

  $scope.getKettleName = function(vid) {
    if ($scope.kettles == undefined) {
      return
    }
    for (i = 0; i < $scope.kettles.length; i++) {
      if (vid == $scope.kettles[i]["key"]) {
        return $scope.kettles[i]["value"];
      }
    }
  }

  $scope.toTimestamp = function(timer) {
    return new Date(timer).getTime();
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

  $scope.clearAllSteps = function() {
    ConfirmMessage.open("Clear Steps", "Do you really want to delete all Steps?", function() {
      CBPSteps.clear({}, function(response) {
        CBPSteps.query({}, function(response) {
          $scope.steps = response.objects
        });
      });
    }, function() {
      // cancel do nothing
    });
  }

  $scope.save_to_book = function() {

    var modalInstance = $uibModal.open({
      animation: true,
      controller: "RecipeBookSave",
      scope: $scope,
      templateUrl: '/base/static/partials/steps/save_recipe.html',
      size: "sm"
    });

    modalInstance.result.then(function(data) {
      CBPRecipeBook.save({
        "name": data.name
      }, function(data) {});
    }, function() {

    });

  }

  $scope.showbook = function() {

    var modalInstance = $uibModal.open({
      animation: true,
      controller: "RecipeBook",
      scope: $scope,
      templateUrl: '/base/static/partials/steps/recipe_book_overview.html',
      size: "sm"
    });

    modalInstance.result.then(function(data) {
      CBPRecipeBook.save({
        "name": data.name
      }, function(data) {});
    }, function() {
      console.log("dismiss");
    });

  }

  $scope.newStep = function() {

    var modalInstance = $uibModal.open({
      animation: true,
      controller: "NewStep",
      scope: $scope,
      templateUrl: '/base/static/partials/steps/form.html',
      size: "sm"
    });

    modalInstance.result.then(function(data) {
      CBPSteps.query({}, function(response) {
        $scope.steps = response.objects;
      });
    }, function() {
      console.log("dismiss");
    });

  }



  $scope.edit = function(id) {
    $scope.selected = id
    var modalInstance = $uibModal.open({
      animation: true,
      controller: "EditStepController",
      scope: $scope,
      templateUrl: '/base/static/partials/steps/form.html',
      size: "sm"
    });
    modalInstance.result.then(function(data) {
      CBPSteps.query(function(response) {
        $scope.steps = response.objects;
      });
    });
  }



})
.controller('EditStepController', function($scope,$uibModalInstance, ConfirmMessage, CBPSteps) {


  $scope.headline = "Edit Step"
  $scope.edit = true;
  CBPSteps.query({}, function(response) {
    $scope.hosts = response.objects;
    CBPSteps.get({
      "id": $scope.selected
    }, function(response) {
      $scope.step = response;
    });
  });

  $scope.save = function() {
    if ($scope.step.name == undefined && $scope.step.name.length == 0) {
      return;
    }
    CBPSteps.update({
      "id": $scope.step.id
    },$scope.step, function(data) {
      $uibModalInstance.close();
    });
  };

  $scope.delete = function() {
    ConfirmMessage.open("Delete Step","Do you really want to delete the step?", function() {
      CBPSteps.delete({
        "id": $scope.step.id
      }, function() {
            $uibModalInstance.close();
      });
    }, function() { });
  }

  $scope.cancel = function() {
    $uibModalInstance.dismiss('cancel');
  };
})
.controller('NewStep', function($scope, CBPSteps, $uibModalInstance, $routeParams, $location) {

  $scope.headline = "New Step"

$scope.edit = false;
  $scope.step = {
    "type": "A",
    "kettleid": 0
  }



  $scope.save = function() {
    if ($scope.step.name == undefined && $scope.step.name.length == 0) {
      return;
    }
    CBPSteps.save($scope.step, function(data) {
      $uibModalInstance.close();
    });
  };

  $scope.cancel = function() {
    $uibModalInstance.dismiss('cancel');
  };


}).controller('KBUploadController', function($scope, $location, CBPSteps, CBPKettle, FileUploader, Braufhelfer, $uibModal) {

  Braufhelfer.get(function(data) {
    $scope.brews = data;
  })
  $scope.load = function(id) {
    $scope.selectKettle(id);
  };

  $scope.uploader = new FileUploader({
    url: '/kbupload',
    queueLimit: 1
  });

  $scope.selectKettle = function(item) {
    var modalInstance = $uibModal.open({
      animation: true,
      templateUrl: '/base/static/partials/steps/select_kettle.html',
      controller: 'KBSelectController',
      size: "sm",
      resolve: {
        kettle: function() {
          return item
        }
      }
    });

    modalInstance.result.then(function(data) {
      Braufhelfer.load(item, data, function() {
        $location.url("/step/overview/");
      });
    }, function() {
      console.log("dismiss");
    });
  };
}).controller('KBSelectController', function($scope, $uibModalInstance, kettle, CBPKettle) {

  $scope.kettles = [];
  $scope.mashtun = 0;
  $scope.boil = 0;
  $scope.kettles.push({
    "key": 0,
    "value": "No Kettle"
  })
  CBPKettle.query({}, function(response) {
    angular.forEach(response.objects, function(d) {
      $scope.kettles.push({
        "key": d.id,
        "value": d.name
      });
    })
  });

  $scope.ok = function() {
    $uibModalInstance.close({
      "mashtun": $scope.mashtun,
      "boil": $scope.boil
    });
  };

  $scope.cancel = function() {
    $uibModalInstance.dismiss('cancel');
  };
});
