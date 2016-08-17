function kettleOverviewController($scope, CBPKettle, $uibModal, ConfirmMessage, CBPHardware) {


    $scope.thermometer = [];
    $scope.thermometer.push({
        "key": "",
        "value": "No Thermometer"
    });


    $scope.automatic = [];
    CBPKettle.getautomatic({}, function (response) {
        $scope.automatic = response;

    });

    $scope.hardware = []
    $scope.hardware.push({
        "key": undefined,
        "value": "NO HARDWARE",
    });

    $scope.hardware_dict = {}

    CBPHardware.query(function (data) {
        data.objects.forEach(function (entry) {

            if (entry.type == 'T') {
                $scope.thermometer.push({
                    "key": entry.id,
                    "value": entry.name
                });
            }
            else {
                $scope.hardware.push({
                    "key": entry.id,
                    "value": entry.name
                });
            }
            $scope.hardware_dict[entry.id] = entry.name;

        });
    });

    CBPKettle.get(function (data) {
        $scope.kettles = data.objects;
    })


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
            CBPKettle.update({
                "id": $scope.kettle.id
            }, $scope.kettle, function () {
                CBPKettle.query({}, function (response) {
                    $scope.kettles = response.objects;
                });
            });
        }, function (data) {
            if ('delete' == data) {
                CBPKettle.delete({
                    "id": $scope.kettle.id
                }, function () {
                    CBPKettle.query({}, function (response) {
                        $scope.kettles = response.objects;
                    });
                });
            }
        });
    }

    $scope.clear = function () {
        ConfirmMessage.open("DELETE_TEMP_LOG", "ARE_YOU_SURE", function () {


            CBPKettle.clear({});


        });
    }


    $scope.master = {
        "name": "",
        "sensorid": "",
        "heater": undefined,
        "agitator": undefined,
    };

    $scope.create = function () {
        $scope.kettle = angular.copy($scope.master);
        $scope.edit_mode = false;

        var modalInstance = $uibModal.open({
            templateUrl: 'static/partials/kettle/form.html',
            controller: 'modalController',
            scope: $scope,
            size: "lg"
        });
        modalInstance.result.then(function () {
            CBPKettle.save($scope.kettle, function (data) {
                CBPKettle.query({}, function (response) {
                    $scope.kettles = response.objects;
                });
            });
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

function kettleCreateController($scope, $uibModalInstance, CBPKettle) {
    $scope.edit = false;
    $scope.save = function () {
        if ($scope.kettle.name != "") {
            CBPKettle.save($scope.kettle, function (data) {
                $uibModalInstance.close();
            });
        }
    };
    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
}


function kettleEditController($scope, $uibModalInstance, CBPKettle, ConfirmMessage) {
    $scope.edit = true;
    $scope.save = function () {

        if ($scope.kettle.name.length == 0) {
            return;
        }

        CBPKettle.update({
            "id": $scope.kettle.id
        }, $scope.kettle, function () {
            $uibModalInstance.close({});
        });
    }
    $scope.delete = function () {

        ConfirmMessage.open("DELETE_KETTLE_HEADLINE", "DELETE_KETTLE_MESSAGE", function () {
            CBPKettle.delete({
                "id": $scope.kettle.id
            }, function () {
                $uibModalInstance.close({});
            });
        }, function () {
        });
    }
    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
}

function ConfirmMessage($route, $location, $uibModal) {

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
        console.log(response);
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


        var modalInstance = $uibModal.open({
            animation: true,
            controller: "HardwareCreateController",
            scope: $scope,
            templateUrl: 'static/partials/hardware/form.html',
            size: "sm"
        });
        modalInstance.result.then(function (data) {
            CBPHardware.query(function (response) {
                $scope.sorthardware(response.objects);
            });
        });
    }

    $scope.edit = function (id) {
        $scope.selected = id
        var modalInstance = $uibModal.open({
            animation: true,
            controller: "HardwareEditController",
            scope: $scope,
            templateUrl: 'static/partials/hardware/form.html',
            size: "sm"
        });
        modalInstance.result.then(function (data) {
            CBPHardware.query(function (response) {
                $scope.sorthardware(response.objects);
            });
        });
    }
}


function HardwareCreateController($scope, CBPHardware, $uibModalInstance) {
    $scope.edit = false;


    $scope.save = function () {

        if ($scope.hardware.name.length == 0) {
            return;
        }
        if ($scope.hardware.type == 'T') {
            delete $scope.hardware.config.switch;
            delete $scope.hardware.config.inverted;
        }

        CBPHardware.save($scope.hardware, function (data) {
            $uibModalInstance.close();
        });
    }
    $scope.cancel = function () {

        $uibModalInstance.dismiss('cancel');
    };

}

function HardwareEditController($scope, CBPHardware, ConfirmMessage, $uibModalInstance, CBPKettle) {

    $scope.edit = true;
    CBPHardware.get({
        "id": $scope.selected
    }, function (response) {
        $scope.hardware = response;
    });

    $scope.save = function () {
        CBPHardware.update({
            "id": $scope.hardware.id
        }, $scope.hardware, function () {
            $uibModalInstance.close({});
        });
    }

    $scope.delete = function () {
        ConfirmMessage.open("Delete Hardware", "Do you really want to delete the hardware?", function () {
            CBPHardware.delete({
                "id": $scope.hardware.id
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

function configController($scope, CBPConfig, $uibModal) {

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

function StepOverviewController($scope, CBPSteps, CBPKettle, $uibModal, ConfirmMessage, CBPRecipeBook) {

    $scope.treeOptions = {
        dropped: function (event) {

            var d = {}
            for (var i = 0; i < $scope.data.length; i++) {
                d[$scope.data[i].id] = i

            }
            CBPSteps.order({}, d)
        },
    };
    $scope.master = {
        "type": "A",
        "state": "I",
        "kettleid": 0
    }

    CBPSteps.query({}, function (response) {
        $scope.data = response.objects;

    });

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
                CBPSteps.query({}, function (response) {
                    $scope.data = response.objects
                });
            });
        });
    }

    $scope.create = function () {

        $scope.step = angular.copy($scope.master);
        var modalInstance = $uibModal.open({
            animation: true,
            controller: "StepCreateController",
            scope: $scope,
            templateUrl: 'static/partials/steps/form.html',
            size: "sm"

        });
        modalInstance.result.then(function (data) {
            CBPSteps.query(function (response) {
                $scope.data = response.objects;
            });
        });
    }

    $scope.edit = function (item) {
        $scope.item = angular.copy(item);
        var modalInstance = $uibModal.open({
            animation: true,
            controller: "StepEditController",
            scope: $scope,
            templateUrl: 'static/partials/steps/form.html',
            size: "sm",

        });
        modalInstance.result.then(function (data) {
            CBPSteps.query(function (response) {
                $scope.data = response.objects;
            });
        });
    }


}


function StepCreateController($scope, CBPSteps, $uibModalInstance) {
    $scope.item = {
        "type": "A",
        "state": "I",
        "kettleid": 0
    }

    $scope.save = function () {
        CBPSteps.save($scope.item, function (data) {
            $uibModalInstance.close();
        });
    }
    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };


}

function StepEditController($scope, CBPSteps, ConfirmMessage, $uibModalInstance, CBPKettle) {

    CBPSteps.get({
        "id": $scope.item.id
    }, function (response) {
        $scope.item = response;
    });

    $scope.edit = true;
    $scope.save = function () {
        CBPSteps.update({
            "id": $scope.item.id
        }, $scope.item, function () {
            $uibModalInstance.close({});
        });
    }

    $scope.delete = function () {
        ConfirmMessage.open("Delete Step", "Do you really want to delete the step?", function () {
            CBPSteps.delete({
                "id": $scope.item.id
            }, function () {
                $uibModalInstance.close();
            });
        });
    }
    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
};

function DashboardMainController($scope, CBPHardware, CBPSteps) {
    $scope.text = "MANUEL";

    $scope.hardware = [];
    $scope.thermometer = [];
    $scope.hardware_dict = {}
    CBPHardware.query(function (data) {

        data.objects.forEach(function (entry) {

            if (entry.config.hide == false) {
                if (entry.type != "T") {
                    $scope.hardware.push(entry);
                }
                else {
                    $scope.thermometer.push(entry);
                }
            }
            $scope.hardware_dict[entry.id] = entry.name;

        });
    });

    CBPSteps.query({}, function (response) {
        $scope.steps = response.objects;


    });

    $scope.$on('socket:step_update', function (ev, data) {
        $scope.steps = data;
    });
}


function DashboardStepController($scope, CBPSteps, ConfirmMessage, mySocket) {


    $scope.next = function () {
        console.log("NEXT");
        mySocket.emit("next");
    }
    $scope.start = function () {
        mySocket.emit("start");
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
        return new Date(timer).getTime();
    }


}

function DashboardKettleController($scope, CBPKettle, ConfirmMessage, mySocket, $uibModal, CBPHardware, CBPSwitch) {

    $scope.$on('socket:temp_udpdate', function (ev, data) {
        $scope.temps = data;
    });
    $scope.$on('socket:kettle_update', function (ev, data) {
        $scope.kettles = data;
    });

    $scope.$on('socket:switch_state_update', function (ev, data) {
        console.log(data);
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

    CBPKettle.get(function (data) {
        $scope.kettles = data.objects;
    });
    CBPKettle.getstate(function (data) {
        $scope.kettle_state = data;
    });

    CBPKettle.getLastTemp(function (data) {
        $scope.temps = data;
    });

    CBPSwitch.get(function (data) {
        $scope.switch_state = data;
    })

    $scope.hardware_dict = {}

    CBPHardware.query(function (data) {
        data.objects.forEach(function (entry) {
            $scope.hardware_dict[entry.id] = entry.name;

        });
    });

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


}

function DashboardHardwareController($scope, mySocket, CBPHardware, CBPSwitch, CBPKettle) {

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

function MainController($scope, CBPConfig, ConfirmMessage, mySocket) {


    $scope.theme = "/base/static/theme.dark.css";
    $scope.$on('socket:config', function (ev, data) {
        $scope.config = data;

    });

    $scope.$on('socket:message', function (ev, data) {

        ConfirmMessage.open(data.headline, data.message, function () {

        });
    });


    $scope.config = {};
    CBPConfig.query(function (data) {
        data.objects.forEach(function (entry) {
            $scope.config[entry.name] = entry.value
        });
    });
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

function ChartController($scope, $routeParams, CBPKettle) {

    $scope.vid = $routeParams.id

    $scope.downsample = function (data, x, y) {

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

    $scope.load = function () {


        CBPKettle.getTemps({
            "id": $scope.vid
        }, function (response) {
            $scope.chart_data = response;

            var chart_data = $scope.downsample(response["temp"], "data", "x");
            var chart_data2 = $scope.downsample(response["target"], "data1", "x1");
            chart_data = chart_data.concat(chart_data2);


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


function FermenterController($scope, $uibModal, CBPFermenter, CBPSwitch, CBPHardware,CBPKettle,mySocket) {


    CBPFermenter.get(function (data) {
        $scope.fermenters = data.objects;
    });
    CBPKettle.getLastTemp(function (data) {
        $scope.temps = data;
    });

    CBPSwitch.get(function (data) {
        $scope.switch_state = data;
    })


    $scope.thermometer = [];
    $scope.thermometer.push({
        "key": "",
        "value": "No Thermometer"
    });
    $scope.hardware = []
    $scope.hardware.push({
        "key": undefined,
        "value": "NO HARDWARE",
    });


    CBPHardware.query(function (data) {
        console.log(data);
        data.objects.forEach(function (entry) {

            if (entry.type == 'T') {
                console.log("PUSH T")
                $scope.thermometer.push({
                    "key": entry.id,
                    "value": entry.name
                });
            }
            else {
                $scope.hardware.push({
                    "key": entry.id,
                    "value": entry.name
                });
            }
            //$scope.hardware_dict[entry.id] = entry.name;

        });
    });

    $scope.$on('socket:fermenter_update', function (ev, data) {
        $scope.fermenters = data;
    });

    $scope.switchGPIO = function (item) {
        mySocket.emit("switch", {"switch": item});
    }

    $scope.$on('socket:switch_state_update', function (ev, data) {
        console.log(data);
        $scope.switch_state = data;
    });

    $scope.$on('socket:temp_udpdate', function (ev, data) {
        $scope.temps = data;
    });

    $scope.create = function (type) {


        $scope.fermenter = {
            "name": "",

        };
        var modalInstance = $uibModal.open({
            animation: true,
            controller: "FermentationCreateController",
            scope: $scope,
            templateUrl: 'static/partials/fermentation/form.html',
            size: "lg"
        });
        modalInstance.result.then(function (data) {
            CBPFermenter.get(function (data) {
                $scope.fermenters = data.objects;
            });
        });
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
        modalInstance.result.then(function (data) {
            CBPFermenter.get(function (data) {
                $scope.fermenters = data.objects;
            });
        });
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

angular.module("cbpcontroller", [])

    .controller("MainController", MainController)
    .controller("kettleOverviewController", kettleOverviewController)
    .controller("kettleCreateController", kettleCreateController)
    .controller("kettleEditController", kettleEditController)

    .controller("HardwareOverviewController", HardwareOverviewController)
    .controller("HardwareCreateController", HardwareCreateController)
    .controller("HardwareEditController", HardwareEditController)

    .controller("configController", configController)
    .controller("configEditController", configEditController)

    .controller("aboutController", aboutController)
    .controller("modalController", modalController)
    .controller("StepOverviewController", StepOverviewController)
    .controller("StepCreateController", StepCreateController)

    .controller("StepEditController", StepEditController)


    .controller("DashboardMainController", DashboardMainController)
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

    .factory("ConfirmMessage", ConfirmMessage);