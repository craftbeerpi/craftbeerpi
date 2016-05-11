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

  var chart_data = $scope.downsample(response["temp"], "data", "x");
  var chart_data2 = $scope.downsample(response["target"], "data1", "x1");
  chart_data =  chart_data.concat(chart_data2);


    console.log(chart_data)

    $scope.chart = c3.generate({
      bindto: '#chart',
      data: {
        xs: {
          data: "x",
          data1: "x1"
        },
        columns: chart_data,
        type: 'area',
        names: {
              data: "Temperature",
              data1: "Target Temperature"
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
        show: false
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
    console.log(data[0][1]);
    console.log(data[0][0]);
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
