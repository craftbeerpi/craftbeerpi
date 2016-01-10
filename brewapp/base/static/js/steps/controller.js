angular.module('myApp.controllers', []).controller('StepOverviewController', function($scope, $location, CBPSteps,CBPKettle, FileUploader, $uibModal, ConfirmMessage) {

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

  $scope.clearAllSteps = function() {
    ConfirmMessage.open("Clear Steps","Do you really want to delete all Steps?", function() {
      CBPSteps.clear({}, function(response) {
        CBPSteps.query({}, function(response) {
          $scope.steps = response.objects
        });
      });
    }, function() {
      // cancel do nothing
    });
  }

  $scope.clear = function() {
    console.log("WOOHo")
    $scope.step = {
      "type": "A",
      "state": "I",
      "kettleid": 0
    }
  }

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
      $scope.step = {
        "type": "A",
        "state": "I",
        "kettleid": 0
      }
    });
  }
  $scope.savenext = function() {
    console.log($scope.step);
    CBPSteps.save($scope.step, function(data) {
      $scope.step = {}
      $location.url("/new/");

    });
  }

}).controller('KBUploadController', function($scope, $location, CBPSteps,CBPKettle, FileUploader, Braufhelfer, $uibModal) {

  Braufhelfer.get(function(data) {
    $scope.brews = data;
  })
  $scope.load = function(id) {

      $scope.selectKettle(id);
      /**/
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
      console.log(data);
      Braufhelfer.load(item, data, function() {
          console.log("OK");
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
  $scope.kettles.push({"key":0, "value":"No Kettle"})
  CBPKettle.query({}, function(response) {
    angular.forEach(response.objects, function(d) {
        $scope.kettles.push({"key":d.id, "value":d.name});
    })
  });

  $scope.ok = function() {
    $uibModalInstance.close({"mashtun": $scope.mashtun, "boil": $scope.boil});
  };

  $scope.cancel = function() {
    $uibModalInstance.dismiss('cancel');
  };
});
