angular.module('craftberpi.controllers3', []).controller('ChartController', function($scope, $location, CBPSteps, CBPKettle, $uibModal, ws, $routeParams) {
  $scope.vid = $routeParams.vid

  CBPKettle.get({
    "id": $scope.vid
  }, function(response) {
    $scope.kettle = response;
  });

  $scope.load = function() {
  CBPKettle.getchart({
    "id": $routeParams.vid
  }, function(response) {

    var chart_data = $scope.downsample(response, "data", "x");
    $scope.chart = c3.generate({
      bindto: '#chart',
      data: {
        xs: {
          data: "x"
        },
        columns: chart_data,
        type: 'area',
        names: {
              data: "Data"
        }
      },
      subchart: {
        show: true
      },
      zoom: {
        rescale: true,
        enabled: true
      },
      point: {
        show: true
      },
      legend: {
        show: false
      },
      grid: {
        x: {
          show: true
        },
        y: {
          show: true
        }
      },
      axis: {
        x: {
          type: 'timeseries',
          tick: {
            format: '%H:%M:%S',
            count: 10
          },
          localtime: true,
          label: 'Time'
        },
        y: {
          label: 'Temperature',
        },

      }

    });


  });
};
  $scope.downsample = function(data, x, y) {
    if (typeof(x) === 'undefined') x = "P1";
    if (typeof(y) === 'undefined') y = "x";

    if (data == undefined) {
      return
    }
    names = [
      [y, x]
    ];
    var down = largestTriangleThreeBuckets(data, 250, 0, 1);
    p1 = [x];
    x = [y];
    for (var i = 0; i < down.length; i++) {

      p1.push(down[i][1]);
      x.push(down[i][0]);
    }
    return [p1, x];
  }

  $scope.load();
});
