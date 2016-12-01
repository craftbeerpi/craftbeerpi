function BaseController($scope, CBPConfig, CBPKettle, CBPHardware, CBPSteps) {

    // Web Socket
    $scope.$on('socket:temp_udpdate', function (ev, data) {
        $scope.temps = data;
    });

    $scope.$on('socket:step_update', function (ev, data) {
        $scope.steps = data;
    });

    // Basic Data
    $scope.thermometer = [];
    $scope.thermometer.push({
        "key": "",
        "value": "No Thermometer"
    });

    $scope.actors = [];

    $scope.hardware = []
    $scope.hardware.push({
        "key": undefined,
        "value": "NO HARDWARE",
    });

    $scope.hardware_dict = {}
    $scope.thermometers = [];

    CBPHardware.query(function (data) {
        data.objects.forEach(function (entry) {

            if (entry.type == 'T') {
                $scope.thermometer.push({
                    "key": entry.id,
                    "value": entry.name
                });
                $scope.thermometers.push(entry);
            }
            else {
                $scope.actors.push(entry);
                $scope.hardware.push({
                    "key": entry.id,
                    "value": entry.name
                });
            }
            $scope.hardware_dict[entry.id] = entry.name;

        });
    });


    $scope.automatic = [];
    CBPKettle.getautomatic({}, function (response) {
        $scope.automatic = response;
    });

    $scope.kettles = [];
    CBPKettle.get(function (data) {
        $scope.kettles = data.objects;
    })

    // Reload Helper
    $scope.kettle_reload = function () {
        CBPKettle.get(function (data) {
            $scope.kettles = data.objects;
        })
    }

    $scope.step_reload = function () {
        CBPSteps.query({}, function (response) {
            $scope.steps = response.objects;
        });
    }


}

function kettleOverviewController($scope, $controller, CBPKettle, $uibModal, ConfirmMessage, CBPHardware) {

    angular.extend(this, $controller('BaseController', {$scope: $scope}));

    $scope.edit = function (item) {
        $scope.kettle = angular.copy(item);
        $scope.edit_mode = true;
        $scope.headline = "DELETE_KETTLE_HEADLINE";
        $scope.message = "DELETE_KETTLE_MESSAGE";
        var modalInstance = $uibModal.open({
            templateUrl: 'static/partials/kettle/form.html',
            controller: 'modalController',
            scope: $scope,
            size: "lg"
        });
        modalInstance.result.then(function () {
            CBPKettle.update({"id": $scope.kettle.id}, $scope.kettle, $scope.kettle_reload);
        }, function (data) {
            if ('delete' == data) {
                CBPKettle.delete({"id": $scope.kettle.id}, $scope.kettle_reload);
            }
        });
    }

    $scope.clear = function () {
        ConfirmMessage.open("DELETE_TEMP_LOG", "ARE_YOU_SURE", CBPKettle.clear);
    }

    $scope.create = function () {
        $scope.kettle = angular.copy({"name": "", "sensorid": "", "heater": undefined, "agitator": undefined});
        $scope.edit_mode = false;
        var modalInstance = $uibModal.open({
            templateUrl: 'static/partials/kettle/form.html',
            controller: 'modalController',
            scope: $scope,
            size: "lg"
        });
        modalInstance.result.then(function () {
            CBPKettle.save($scope.kettle, $scope.kettle_reload);
        });
    }
};

function modalController($scope, $uibModalInstance, ConfirmMessage) {
    $scope.ok = function () {
        $uibModalInstance.close($scope);
    };
    $scope.delete = function () {
        ConfirmMessage.open($scope.headline, $scope.message, function () {
            $uibModalInstance.dismiss('delete');
        });
    };
    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
}


function ConfirmMessage($location, $uibModal) {

    return {
        open: function (headline, message, confirm, cancel) {

            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'static/partials/common/confirm.html',
                controller: 'ConfirmController',
                size: "sm",
                resolve: {
                    headline: function () {
                        return headline
                    },
                    message: function () {
                        return message
                    }
                }
            });
            modalInstance.result.then(function (data) {
                if (confirm != undefined) {
                    confirm()
                }
            }, function () {
                if (cancel != undefined) {
                    cancel()
                }

            })
        }
    }
}

function ConfirmController($scope, $uibModalInstance, headline, message) {
    $scope.message = message;
    $scope.headline = headline;
    $scope.ok = function () {
        $uibModalInstance.close();
    };
    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
}


function HardwareOverviewController($scope, CBPHardware, CBPKettle, $uibModal) {

    $scope.heater = [];
    $scope.pump = [];
    $scope.agitator = [];
    $scope.other = [];
    $scope.thermometer = [];
    $scope.type = [
        {"key": "P", "value": "PUMP"},
        {"key": "A", "value": "AGITATOR"},
        {"key": "H", "value": "HEATER"},
        {"key": "T", "value": "THERMOMETER"},
        {"key": "O", "value": "OTHER"},
    ];

    // Get GPIOs
    $scope.gpio = []
    CBPKettle.getDevices({}, function (response) {

        angular.forEach(response, function (d) {
            $scope.gpio.push({
                "key": d,
                "value": d
            });
        })
    });

    $scope.sorthardware = function (data) {

        $scope.heater = [];
        $scope.pump = [];
        $scope.agitator = [];
        $scope.other = [];
        $scope.thermometer = [];
        angular.forEach(data, function (d) {
            switch (d.type) {
                case "H":
                    $scope.heater.push(d);
                    break;
                case "P":
                    $scope.pump.push(d);
                    break;
                case "A":
                    $scope.agitator.push(d);
                    break;
                case "T":
                    $scope.thermometer.push(d);
                    break;
            }

        });
    }

    $scope.sensors = [];

    CBPKettle.getthermometer({}, function (response) {
        angular.forEach(response, function (d) {
            $scope.sensors.push({
                "key": d,
                "value": d
            });
        })
    });

    CBPHardware.query(function (response) {
        $scope.sorthardware(response.objects);
        $scope.hw = response.objects;
    });

    $scope.createHardware = function (type) {

        if (type == 'T') {
            $scope.hardware = {
                "name": "",
                "type": type,
                "config": {
                    "thermometer": {"offset": 0},
                    "hide": false
                }
            };
        }
        else {
            $scope.hardware = {
                "name": "",
                "type": type,
                "config": {
                    "inverted": false,
                    "hide": false
                }
            };
        }

        $scope.edit_mode = false;
        var modalInstance = $uibModal.open({
            animation: true,
            controller: "modalController",
            scope: $scope,
            templateUrl: 'static/partials/hardware/form.html',
            size: "sm"
        });
        modalInstance.result.then(function (data) {


            if ($scope.hardware.type == 'T') {
                delete $scope.hardware.config.switch;
                delete $scope.hardware.config.inverted;
            }

            CBPHardware.save($scope.hardware, function (data) {
                CBPHardware.query(function (response) {
                    $scope.sorthardware(response.objects);
                });
            });

        });
    }

    $scope.edit = function (item) {
        $scope.edit_mode = true;
        $scope.hardware = angular.copy(item);
        $scope.headline = "DELETE_KETTLE_HEADLINE";
        $scope.message = "DELETE_KETTLE_MESSAGE";
        var modalInstance = $uibModal.open({
            animation: true,
            controller: "modalController",
            scope: $scope,
            templateUrl: 'static/partials/hardware/form.html',
            size: "sm"
        });
        modalInstance.result.then(function (data) {

            CBPHardware.update({
                "id": $scope.hardware.id
            }, $scope.hardware, function () {
                CBPHardware.query(function (response) {
                    $scope.sorthardware(response.objects);
                });
            });
        }, function (data) {
            if ('delete' == data) {
                CBPHardware.delete({
                    "id": $scope.hardware.id
                }, function () {
                    CBPHardware.query(function (response) {
                        $scope.sorthardware(response.objects);
                    });
                });
            }
        });

    }
}

function configController($scope, $controller, CBPConfig, $uibModal) {

    angular.extend(this, $controller('BaseController', {$scope: $scope}));
    CBPConfig.query({}, function (response) {
        $scope.configparams = response.objects;
    });

    $scope.edit = function (item) {
        $scope.item = angular.copy(item);
        var modalInstance = $uibModal.open({
            animation: true,
            controller: "configEditController",
            scope: $scope,
            templateUrl: 'static/partials/config/form.html',
            size: "sm",

        });
        modalInstance.result.then(function (data) {
            CBPConfig.query({}, function (response) {
                $scope.configparams = response.objects;
            });
        });
    }

}

function configEditController($scope, $uibModalInstance, CBPConfig) {

    $scope.name = $scope.selected;
    CBPConfig.get({
        "name": $scope.item.name
    }, function (response) {
        $scope.configparam = response;

        if ($scope.configparam.options != null) {
            $scope.options = $scope.configparam.options.split(',');
        }
    });
    $scope.save = function () {
        CBPConfig.update({
            "name": $scope.item.name
        }, $scope.item, function () {
            $uibModalInstance.close({});
        });
    }
    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
}


function aboutController($scope, ConfirmMessage, $translate, $window) {

    $scope.restart = function () {
        ConfirmMessage.open("Shutdown", "Are you sure to restart CraftBeerPi?", function () {
            $window.location.href = '/restart';
        });
    }

    $scope.confirmHalt = function () {
        ConfirmMessage.open("Shutdown", "Are you sure to shutdown CraftBeerPi?", function () {
            $window.location.href = '/halt';
        });
    }

    $scope.changeLanguage = function (langKey) {
        $scope.language = langKey;
        $translate.use(langKey);
    };
}

function StepOverviewController($scope, $controller, CBPSteps, CBPKettle, $uibModal, ConfirmMessage, CBPRecipeBook) {

    angular.extend(this, $controller('BaseController', {$scope: $scope}));

    $scope.steps = []
    CBPSteps.query({}, function (response) {
        $scope.steps = response.objects;

    });

    $scope.treeOptions = {
        dropped: function (event) {

            var d = {}
            for (var i = 0; i < $scope.steps.length; i++) {
                d[$scope.steps[i].id] = i

            }
            CBPSteps.order({}, d)
        },
    };

    $scope.kettles = [];
    $scope.kettles_name = {};
    CBPKettle.query({}, function (response) {
        angular.forEach(response.objects, function (d) {
            $scope.kettles.push({
                "key": d.id,
                "value": d.name
            });
            $scope.kettles_name[d.id] = d.name;
        })
    });

    $scope.recipebook = function () {

        var modalInstance = $uibModal.open({
            animation: true,
            controller: "RecipeBook",
            scope: $scope,
            templateUrl: 'static/partials/steps/recipe_book_overview.html',
            size: "sm"
        });

        modalInstance.result.then(function (data) {
            CBPRecipeBook.save({
                "name": data.name
            }, function (data) {
            });
        }, function () {

        });

    }

    $scope.recipebook_save = function () {

        var modalInstance = $uibModal.open({
            animation: true,
            controller: "RecipeBookSave",
            scope: $scope,
            templateUrl: 'static/partials/steps/save_recipe.html',
            size: "sm"
        });

        modalInstance.result.then(function (data) {
            CBPRecipeBook.save({
                "name": data.name
            }, function (data) {
            });
        }, function () {

        });

    }


    $scope.clear = function () {
        ConfirmMessage.open("CLEAR_STEPS_HEADLINE", "ARE_YOU_SURE", function () {
            CBPSteps.clear({}, function (response) {
                $scope.steps = []

            });
        });
    }

    $scope.create = function () {
        console.log("NEW")
        $scope.item = angular.copy({"type": "A", "state": "I", "kettleid": 0});
        $scope.edit_mode = false;
        $scope.headline = "CREATE_STEP";
        var modalInstance = $uibModal.open({
            templateUrl: 'static/partials/steps/form.html',
            controller: 'modalController',
            scope: $scope,
            size: "sm"
        });
        modalInstance.result.then(function () {
            CBPSteps.save($scope.item, $scope.step_reload);
        });
    }


    $scope.edit = function (item) {
        $scope.edit_mode = true;
        $scope.item = angular.copy(item);
        $scope.headline = "EDIT_STEP";

        var modalInstance = $uibModal.open({
            animation: true,
            controller: "modalController",
            scope: $scope,
            templateUrl: 'static/partials/steps/form.html',
            size: "sm"
        });
        modalInstance.result.then(function (data) {

            CBPSteps.update({
                "id": $scope.item.id
            }, $scope.item, $scope.step_reload);

        }, function (data) {
            if ('delete' == data) {
                CBPSteps.delete({
                    "id": $scope.item.id
                }, $scope.step_reload);
            }
        });

    }
}




function DashboardStepController($scope, $rootScope, CBPSteps, ConfirmMessage, mySocket) {

    $scope.steps = [];
    $scope.running = false;

    function check_running(data) {
         $scope.running = false;
         for (var d in data) {

            if(data[d].state != 'I') {
                $scope.running = true;
                break;
            }
        };
    }

    CBPSteps.query({}, function (response) {
        $scope.steps = response.objects;
        check_running(response.objects);
    });


    $scope.$on('socket:step_update', function (ev, data) {
        check_running(data);

        console.log(data)
        $scope.steps = data;
    });




    $scope.next = function () {
        mySocket.emit("next");
    }

    $scope.start = function () {
        mySocket.emit("start");
    }

    $scope.start_timer = function () {
        mySocket.emit("start_timer_current_step");
    }

    $scope.reset = function () {
        ConfirmMessage.open("RESET_BREWING_PROCESS", "ARE_YOU_SURE", function () {
            mySocket.emit("reset");
        });
    }

    $scope.reset_current = function () {
        ConfirmMessage.open("RESET_CURRENT_STEP", "ARE_YOU_SURE", function () {
            mySocket.emit("reset_current_step");
        });
    }



     $scope.toTimestamp = function (timer) {
        if (timer == undefined)
            return
        return new Date(timer).getTime();
    }


}

function DashboardKettleController($scope, $controller, CBPKettle, ConfirmMessage, mySocket, $uibModal, CBPHardware, CBPSwitch) {


    angular.extend(this, $controller('BaseController', {$scope: $scope}));


    $scope.$on('socket:kettle_update', function (ev, data) {
        $scope.kettles = data;
    });

    $scope.$on('socket:switch_state_update', function (ev, data) {
        $scope.switch_state = data;
    });
    $scope.$on('socket:kettle_state_update', function (ev, data) {
        $scope.kettle_state = data;
    });


    $scope.switchGPIO = function (item) {
        mySocket.emit("switch", {"switch": item});
    }

    $scope.switch_automatic = function (item) {
        CBPKettle.automatic({"id": item.id});
    }

    CBPKettle.getstate(function (data) {
        $scope.kettle_state = data;
    });

    CBPKettle.getLastTemp(function (data) {
        $scope.temps = data;
    });

    CBPSwitch.get(function (data) {
        $scope.switch_state = data;
    })

    $scope.setTargetTemp = function (item) {
        $scope.kettle = item;
        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'static/partials/dashboard/target_temp.html',
            controller: 'TargetTempController',
            size: "sm",
            scope: $scope

        });
    };

    $scope.calcVolume = function (item) {
        $scope.kettle = item;

        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'static/partials/dashboard/volume.html',
            controller: 'VolumeController',
            size: "sm",
            scope: $scope,

        });
    };

    $scope.create = function () {

        $scope.kettle = angular.copy({"name": "", "sensorid": "", "heater": undefined, "agitator": undefined});
        $scope.edit_mode = false;
        var modalInstance = $uibModal.open({
            animation: false,
            templateUrl: 'static/partials/kettle/form.html',
            controller: 'modalController',
            scope: $scope,
            size: "lg"
        });
        modalInstance.result.then(function () {
            CBPKettle.save($scope.kettle, $scope.kettle_reload);
        });
    }

    $scope.edit = function (item) {
        $scope.kettle = angular.copy(item);
        $scope.edit_mode = true;
        $scope.headline = "DELETE_KETTLE_HEADLINE";
        $scope.message = "DELETE_KETTLE_MESSAGE";
        var modalInstance = $uibModal.open({
            animation: false,
            templateUrl: 'static/partials/kettle/form.html',
            controller: 'modalController',
            scope: $scope,
            size: "lg"
        });
        modalInstance.result.then(function () {
            CBPKettle.update({"id": $scope.kettle.id}, $scope.kettle, $scope.kettle_reload);
        }, function (data) {
            if ('delete' == data) {
                CBPKettle.delete({"id": $scope.kettle.id}, $scope.kettle_reload);
            }
        });
    }
}

function DashboardHardwareController($scope, $controller, mySocket, CBPHardware, CBPSwitch, CBPKettle) {

    angular.extend(this, $controller('BaseController', {$scope: $scope}));


    CBPSwitch.get(function (data) {
        $scope.switch_state = data;
    })

    $scope.$on('socket:temp_udpdate', function (ev, data) {
        $scope.temps = data;
    });

    $scope.$on('socket:switch_state_update', function (ev, data) {

        $scope.switch_state = data;
    });

    $scope.switchGPIO = function (item) {
        mySocket.emit("switch", {"switch": item});
    }

    $scope.switch_for_seconds = function (s) {
        console.log("HALLO")
        mySocket.emit("switch_for_seconds", {"switch": s, "seconds": 5});
    }


    CBPKettle.getLastTemp(function (data) {
        $scope.temps = data;
    });


}


function TargetTempController($scope, $uibModalInstance, CBPKettle) {
    $scope.save = function () {
        CBPKettle.targettemp({"id": $scope.kettle.id}, {"temp": $scope.target_temp});
        $uibModalInstance.close();

    }
    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
}

function KBHController($scope, $location, CBPSteps, CBPKettle, FileUploader, Braufhelfer, $uibModal) {

    Braufhelfer.get(function (data) {
        $scope.brews = data;
    })
    $scope.load = function (id) {
        $scope.selectKettle(id);
    };

    $scope.uploader = new FileUploader({
        url: '/kbupload',
        queueLimit: 1,
        onCompleteAll: function () {
            Braufhelfer.get(function (data) {
                $scope.brews = data;
            })
        }
    });


    $scope.upload = function () {
        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'static/partials/kbh/upload.html',
            controller: 'KBHUploadController',
            size: "sl",

        });

        modalInstance.result.then(function (data) {
            Braufhelfer.get(function (data) {
                $scope.brews = data;
            })
        });
    }

    $scope.selectKettle = function (item) {
        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'static/partials/kbh/select_kettle.html',
            controller: 'KBHSelectController',
            size: "sm",
            resolve: {
                kettle: function () {
                    return item
                }
            }
        });

        modalInstance.result.then(function (data) {
            Braufhelfer.load(item, data, function () {
                $location.url("/steps/");
            });
        }, function () {

        });
    };
}

function KBHUploadController($scope, $uibModalInstance, Braufhelfer, CBPKettle, FileUploader) {


    $scope.uploader = new FileUploader({
        url: '/kbupload',
        queueLimit: 1,
        onCompleteAll: function () {
            Braufhelfer.get(function (data) {
                $scope.brews = data;
            })
        }
    });

    $scope.ok = function () {
        $uibModalInstance.close();
    };

    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
}

function KBHSelectController($scope, $uibModalInstance, kettle, CBPKettle) {

    $scope.kettles = [];
    $scope.mashtun = 0;
    $scope.boil = 0;
    $scope.kettles.push({
        "key": 0,
        "value": "No Kettle"
    })
    CBPKettle.query({}, function (response) {
        angular.forEach(response.objects, function (d) {
            $scope.kettles.push({
                "key": d.id,
                "value": d.name
            });
        })
    });

    $scope.ok = function () {
        $uibModalInstance.close({
            "mashtun": $scope.mashtun,
            "boil": $scope.boil
        });
    };

    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
}


function RecipeBook($scope, $location, $uibModalInstance, CBPRecipeBook, ConfirmMessage) {

    CBPRecipeBook.query({}, function (response) {
        $scope.items = response.objects;
    });

    $scope.load = function (id) {

        CBPRecipeBook.load({
            "id": id
        }, function (data) {
            $location.url("/steps/");
        });
    };

    $scope.delete = function (id) {

        ConfirmMessage.open("Delete Recipe", "Are you sure?", function () {
            CBPRecipeBook.delete({
                "id": id
            }, function () {
                CBPRecipeBook.query({}, function (response) {
                    $scope.items = response.objects;
                });
            });
        });


    };

    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };


}


function RecipeBookSave($scope, $location, CBPConfig, $uibModalInstance, ConfirmMessage, CBPRecipeBook) {


    $scope.name = "";
    $scope.save = function () {
        $uibModalInstance.close({"name": $scope.name});
    };

    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
}


function VolumeController($scope, $uibModalInstance) {
    $scope.free = 0

    function Round(v) {
        return ("" + (Math.round(v * 100) / 100)).replace(/\./g, ",");
    }

    $scope.volume = function () {

        var maxHeight = parseFloat($scope.kettle.height);
        var free = parseFloat($scope.free);
        var height = maxHeight - free;
        var radius = parseFloat($scope.kettle.diameter) / 2.0;
        return Round(Math.PI * radius * radius * height / 1000.0);
    }

    $scope.maxvolume = function () {
        var maxHeight = parseFloat($scope.kettle.height);
        var radius = parseFloat($scope.kettle.diameter) / 2.0;
        return Round(Math.PI * radius * radius * maxHeight / 1000.0);
    }
    $scope.ok = function () {
        $uibModalInstance.close();
    };
    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
};


function ChartController($scope, CBPChart, $state, $stateParams) {

    $scope.vid = $stateParams.id;

    $scope.type = $state.current.type;


    $scope.load = function () {
        $scope.loading = true;
        var legends = undefined;
        CBPChart.get($state.current.type +$scope.vid
            , function (response) {

                 $scope.loading = false;

            var options = {
             series: {
				lines: { show: true },
				points: { show: false },
			},
			xaxis: {
				mode: "time",
				tickLength: 5
			},
                crosshair: {
				mode: "x"
			},grid: {
				hoverable: true,
                    backgroundColor: '#fff',
				autoHighlight: true
			},
			selection: {
				mode: "x"
			},

		    };

		    var plot = $.plot("#placeholder", [{data:response.temp, label: "Temp = -0.00"}, {data:response.target_temp, label: "TagetTemp = -0.00"}], options);

            legends = $("#placeholder .legendLabel");
            legends.each(function () {
			    // fix the widths so they don't jump around
			    $(this).css('width', $(this).width());
		    });

            var updateLegendTimeout = null;
		var latestPosition = null;

		function updateLegend() {


			updateLegendTimeout = null;

			var pos = latestPosition;

			var axes = plot.getAxes();
			if (pos.x < axes.xaxis.min || pos.x > axes.xaxis.max ||
				pos.y < axes.yaxis.min || pos.y > axes.yaxis.max) {

				return;
			}

			var i, j, dataset = plot.getData();
			for (i = 0; i < dataset.length; ++i) {

				var series = dataset[i];
				// Find the nearest points, x-wise
				for (j = 0; j < series.data.length; ++j) {
					if (series.data[j][0] > pos.x) {
						break;
					}
				}
				// Now Interpolate
				var y,
					p1 = series.data[j - 1],
					p2 = series.data[j];

				if (p1 == null) {
					y = p2[1];
				} else if (p2 == null) {
					y = p1[1];
				} else {
					y = p1[1] + (p2[1] - p1[1]) * (pos.x - p1[0]) / (p2[0] - p1[0]);
				}

				legends.eq(i).text(series.label.replace(/=.*/, "= " + y.toFixed(2)));
			}
		}

		$("#placeholder").bind("plothover",  function (event, pos, item) {
			latestPosition = pos;
			if (!updateLegendTimeout) {
				updateLegendTimeout = setTimeout(updateLegend, 50);
			}
		});

		var overview = $.plot("#overview", [response.temp, response.target_temp], {
			series: {
				lines: {
					show: true,
					lineWidth: 1
				},

				shadowSize: 0
			},
            grid: {
                backgroundColor: '#fff'
            },
			xaxis: {
				ticks: [],
				mode: "time"
			},
			yaxis: {
				ticks: [],
				min: 0,
				autoscaleMargin: 0.1
			},
			selection: {
				mode: "x"
			}
		});

		// now connect the two

		$("#placeholder").bind("plotselected", function (event, ranges) {


			// do the zooming
			$.each(plot.getXAxes(), function(_, axis) {
				var opts = axis.options;
				opts.min = ranges.xaxis.from;
				opts.max = ranges.xaxis.to;
			});
			plot.setupGrid();
			plot.draw();
			plot.clearSelection();

			// don't fire event on the overview to prevent eternal loop
			overview.setSelection(ranges, true);
            legends = $("#placeholder .legendLabel");
            updateLegendTimeout = null;
            latestPosition = null;

            $("#placeholder").bind("plothover",  function (event, pos, item) {

			    latestPosition = pos;
			    if (!updateLegendTimeout) {
				    updateLegendTimeout = setTimeout(updateLegend, 50);
			    }
		    });
		});

        var placeholder = $("#placeholder");

		$("#overview").bind("plotselected", function (event, ranges) {

			plot.setSelection(ranges);
		});

        });

    }

    $scope.clear = function () {
        CBPChart.delete("K_"+$scope.vid, function () {
            $("#placeholder").empty();
            $("#overview").empty();
        });

    }

    $scope.back = function () {
        console.log($state.current)
        $state.go($state.current.back)
    }

    $scope.load();
}


function setupController($scope, $translate, CBPSetup, $window, $location, WizardHandler) {


    var i = 1
    $scope.brewery = {"name": ""};
    $scope.heater = [];
    $scope.agitator = [];
    $scope.thermometer = [];
    $scope.pump = [];
    $scope.kettle = [];


    $scope.dump = function () {
        console.log($scope.brewery);
    }


    $scope.next = function () {

        switch (WizardHandler.wizard().currentStepNumber()) {

            case 5:
                $scope.startKettleStep();
                break;
            default:
                WizardHandler.wizard().next();
                break;
        }


    }

    $scope.changeLanguage = function (langKey) {
        $scope.language = langKey;
        $translate.use(langKey);
    };

    $scope.setThermometer = function (type) {

        CBPSetup.thermometer({"type": type}, function (response) {
            $scope.sensors = []

            angular.forEach(response, function (d) {
                $scope.sensors.push({"key": d, "value": d});
            });
            WizardHandler.wizard().next();
        });

    }

    $scope.setHardware = function (type) {

        CBPSetup.hardware({"type": type}, function (response) {
            $scope.gpio = []
            angular.forEach(response, function (d) {
                $scope.gpio.push({"key": d, "value": d});
            });

            WizardHandler.wizard().next();
        });

    }

    $scope.showNext = function () {

        switch (WizardHandler.wizard().currentStepNumber()) {
            case 1:
            case 3:
            case 4:
            case 7:
                return false;
                break;
            default:
                return true;
                break;
        }
    }

    $scope.showBack = function () {

        if (WizardHandler.wizard().currentStepNumber() > 1) {
            return true;
        }
        else {
            return false;
        }
    }

    $scope.back = function () {
        console.log();
        WizardHandler.wizard().previous();
    }

    $scope.startKettleStep = function () {
        var i = 0;
        $scope.hardware = $scope.heater.concat($scope.agitator).concat($scope.pump);

        WizardHandler.wizard().next();

    }

    $scope.add = function (type) {

        switch (type) {
            case 'H':
                $scope.heater.push({
                    "id": i++,
                    "name": "Heater",
                    "type": "H",
                    "config": {"inverted": false, "hide": false}
                });
                break;
            case 'A':
                $scope.agitator.push({
                    "id": i++,
                    "name": "Agiator",
                    "type": "A",
                    "config": {"inverted": false, "hide": false}
                });
                break;
            case 'P':
                $scope.pump.push({
                    "id": i++,
                    "name": "Pump",
                    "type": "P",
                    "config": {"inverted": false, "hide": false}
                });
                break;
            case 'T':
                $scope.thermometer.push({
                    "id": i++,
                    "name": "Thermometer",
                    "type": "T",
                    "config": {"hide": false, "thermometer": {"offset": 0}}
                });
                break;
            case 'K':
                $scope.kettle.push({"name": "Kettle1"});
                break;
        }
    }

    $scope.remove = function (index, type) {
        switch (type) {
            case 'H':
                $scope.heater.splice(index, 1);
                break;
            case 'A':
                $scope.agitator.splice(index, 1);
                break;
            case 'P':
                $scope.pump.splice(index, 1);
                break;
            case 'T':
                $scope.thermometer.splice(index, 1);
                break;
            case 'K':
                $scope.kettle.splice(index, 1);
                break;
        }
    }

    $scope.finish = function () {

        var hw = $scope.heater.concat($scope.agitator).concat($scope.pump).concat($scope.thermometer);

        CBPSetup.setup({}, {
            "hardware": hw,
            "kettle": $scope.kettle,
            "brewery_name": $scope.brewery.name
        }, function (response) {
            $window.location.href = "/";
        });
    }


}

function FermenterController($scope, $uibModal, $controller, CBPHydrometer, CBPFermenter, CBPFermenterSteps, CBPSwitch, CBPHardware, CBPKettle, mySocket) {

    angular.extend(this, $controller('BaseController', {$scope: $scope}));

    $scope.fermenters = {};
    $scope.state = {};
    CBPFermenter.state(function (data) {

        $scope.state = data;
    });


    CBPHydrometer.get(function(data) {
      console.log(data);
        $scope.hydrometer = data;
    })


    function compare(a, b) {
        if (a.order < b.order)
            return -1;
        if (a.order > b.order)
            return 1;
        return 0;
    }


    $scope.toTimestamp = function (timer) {
        if (timer == undefined)
            return
        return new Date(timer).getTime();
    }

    $scope.getTimer = function (n) {

        start = new Date(n.start).getTime();
        day_seconds = n.days * 24 * 60 * 60 * 1000;
        hour_seconds = n.hours * 60 * 60 * 1000;
        minutes_seconds = n.minutes * 60 * 1000;
        return start + day_seconds + hour_seconds + minutes_seconds;

    }

    $scope.parseFloat = function (number) {
        return parseFloat(number, 0);
    }

    $scope.treeOptions = function (id) {
        return {
            accept: function (sourceNodeScope, destNodesScope, destIndex) {
                console.log("ID");
                if (sourceNodeScope.$treeScope != destNodesScope.$treeScope) {
                    return false;
                } else {
                    return true;
                }
            },
            dropped: function (event) {
                var data = event.dest.nodesScope['$modelValue'];
                var d = {}
                for (var i = 0; i < data.length; i++) {
                    console.log(data[i]);
                    d[data[i].id] = i
                }
                CBPFermenter.order({}, {"id": id, "steps": d});
            }
        }
    };

    reload = function () {
        CBPFermenter.get(function (data) {

            data.objects.map(function (obj) {
                $scope.fermenters[obj.id] = obj;
            });

        });
    }

    reload();

    CBPKettle.getLastTemp(function (data) {
        $scope.temps = data;
    });

    CBPSwitch.get(function (data) {
        $scope.switch_state = data;
    })

    $scope.$on('socket:fermenter_update', function (ev, data) {

        $scope.fermenters[data.id] = data;

    });

    $scope.switchGPIO = function (item) {
        mySocket.emit("switch", {"switch": item});
    }

    $scope.$on('socket:switch_state_update', function (ev, data) {
        $scope.switch_state = data;
    });

    $scope.$on('socket:fermenter_state_update', function (ev, data) {
        $scope.state = data;
    });


    $scope.getTime = function (item) {

        return (item.days * 86400 + item.hours * 3600 + item.minutes * 60);

    }

    $scope.create = function (type) {
        $scope.fermenter = {
            "name": "",
            "cooleroffset_min": 0.5,
            "cooleroffset_max": 0.2,
            "heateroffset_min": 0.5,
            "heateroffset_max": 0.2


        };
        var modalInstance = $uibModal.open({
            animation: true,
            controller: "FermentationCreateController",
            scope: $scope,
            templateUrl: 'static/partials/fermentation/form.html',
            size: "lg"
        });
        modalInstance.result.then(reload);
    }

    $scope.edit = function (id) {
        $scope.selected = id
        var modalInstance = $uibModal.open({
            animation: true,
            controller: "FermentationEditController",
            scope: $scope,
            templateUrl: 'static/partials/fermentation/form.html',
            size: "lg"
        });
        modalInstance.result.then(reload);
    }

    $scope.setTargetTemp = function (item) {
        $scope.fermenter = item;
        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'static/partials/fermentation/target_temp.html',
            controller: 'FermenationTargetTempController',
            size: "sm",
            scope: $scope

        });
    };

    $scope.switchAutomatic = function (item) {
        CBPFermenter.automatic({"id": item.id})
    }

    $scope.start = function (item) {
        CBPFermenter.start({"id": item.id})
    }

    $scope.stop = function (item) {
        CBPFermenter.stop({"id": item.id})
    }

    $scope.next = function (item) {
        CBPFermenter.next({"id": item.id})
    }

    $scope.reset = function (item) {
        CBPFermenter.reset({"id": item.id})
    }

    $scope.editStep = function (item) {
        $scope.edit_mode = true;
        $scope.item = angular.copy(item);
        $scope.headline = "DELETE_KETTLE_HEADLINE";
        $scope.message = "DELETE_KETTLE_MESSAGE";
        var modalInstance = $uibModal.open({
            animation: true,
            controller: "modalController",
            scope: $scope,
            templateUrl: 'static/partials/fermentation/stepform.html',
            size: "sm"
        });
        modalInstance.result.then(function (data) {

            CBPFermenterSteps.update({
                "id": $scope.item.id
            }, $scope.item, reload);

        }, function (data) {
            if ('delete' == data) {
                CBPFermenterSteps.delete({
                    "id": $scope.item.id
                }, reload);
            }
        });

    }

    $scope.createStep = function (item) {

        $scope.item = angular.copy({
            "name": "",
            "fermenter_id": item.id,
            "temp": 0,
            "days": 0,
            "minutes": 0,
            "hours": 0,
            "state": "I"
        });
        $scope.edit_mode = false;
        var modalInstance = $uibModal.open({
            templateUrl: 'static/partials/fermentation/stepform.html',
            controller: 'modalController',
            scope: $scope,
            size: "sm"
        });
        modalInstance.result.then(function () {
            console.log($scope.item);
            CBPFermenterSteps.save($scope.item, reload);
        });
    }
}

function FermentationCreateController($scope, CBPFermenter, $uibModalInstance) {
    $scope.edit = false;
    $scope.save = function () {
        if ($scope.fermenter.name != "") {
            CBPFermenter.save($scope.fermenter, function (data) {
                $uibModalInstance.close();
            });
        }
    };
    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
}

function FermentationEditController($scope, ConfirmMessage, $uibModalInstance, CBPFermenter) {

    $scope.edit = true;
    CBPFermenter.get({
        "id": $scope.selected
    }, function (response) {
        $scope.fermenter = response;
    });


    $scope.save = function () {
        CBPFermenter.update({
            "id": $scope.fermenter.id
        }, $scope.fermenter, function () {
            $uibModalInstance.close({});
        });
    }

    $scope.delete = function () {
        ConfirmMessage.open("Delete Hardware", "Do you really want to delete the hardware?", function () {
            CBPFermenter.delete({
                "id": $scope.fermenter.id
            }, function () {
                $uibModalInstance.close();
            });
        }, function () {
        });
    }
    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
};

function FermenationTargetTempController($scope, $uibModalInstance, CBPFermenter) {
    $scope.save = function () {
        CBPFermenter.targettemp({"id": $scope.fermenter.id}, {"temp": $scope.target_temp});
        $uibModalInstance.close();

    }
    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
}

function FermenationStepController($scope, $uibModal, CBPFermenter, CBPFermenterSteps) {




    var reload = function () {
        CBPFermenter.get({"id": $routeParams.id}, function (data) {

            console.log(data);
            $scope.fermentation_steps = data.steps;
        });
    }

    reload();

    $scope.create = function () {

        $scope.item = angular.copy({
            "name": "",
            "fermenter_id": $routeParams.id,
            "temp": 0,
            "days": 0,
            "minutes": 0,
            "hours": 0
        });
        $scope.edit_mode = false;
        var modalInstance = $uibModal.open({
            templateUrl: 'static/partials/fermentation/stepform.html',
            controller: 'modalController',
            scope: $scope,
            size: "sm"
        });
        modalInstance.result.then(function () {
            console.log($scope.item);
            CBPFermenterSteps.save($scope.item, reload);

        });
    }

    $scope.edit = function (item) {
        $scope.edit_mode = true;
        $scope.item = angular.copy(item);
        $scope.headline = "DELETE_KETTLE_HEADLINE";
        $scope.message = "DELETE_KETTLE_MESSAGE";
        var modalInstance = $uibModal.open({
            animation: true,
            controller: "modalController",
            scope: $scope,
            templateUrl: 'static/partials/fermentation/stepform.html',
            size: "sm"
        });
        modalInstance.result.then(function (data) {

            CBPFermenterSteps.update({
                "id": $scope.item.id
            }, $scope.item, reload);

        }, function (data) {
            if ('delete' == data) {
                CBPFermenterSteps.delete({
                    "id": $scope.item.id
                }, reload);
            }
        });

    }

}


angular.module("cbpcontroller", [])
    .controller("BaseController", BaseController)
    .controller("HardwareOverviewController", HardwareOverviewController)
    .controller("configController", configController)
    .controller("configEditController", configEditController)
    .controller("aboutController", aboutController)
    .controller("modalController", modalController)
    .controller("StepOverviewController", StepOverviewController)
    .controller("DashboardStepController", DashboardStepController)
    .controller("DashboardKettleController", DashboardKettleController)
    .controller("DashboardHardwareController", DashboardHardwareController)
    .controller("TargetTempController", TargetTempController)
    .controller("VolumeController", VolumeController)
    .controller("ChartController", ChartController)
    .controller("KBHController", KBHController)
    .controller("KBHSelectController", KBHSelectController)
    .controller("KBHUploadController", KBHUploadController)
    .controller("RecipeBook", RecipeBook)
    .controller("RecipeBookSave", RecipeBookSave)
    .controller("ConfirmController", ConfirmController)
    .controller("setupController", setupController)
    .controller("FermenterController", FermenterController)
    .controller("FermentationCreateController", FermentationCreateController)
    .controller("FermentationEditController", FermentationEditController)
    .controller("FermenationTargetTempController", FermenationTargetTempController)
    .controller("FermenationStepController", FermenationStepController)
    .factory("ConfirmMessage", ConfirmMessage);