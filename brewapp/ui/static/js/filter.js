function hardware_icon() {
    return function (input) {
        switch (input) {
            case "H":
                return "fa-fire";
                break;
            case "A":
                return "fa-refresh";
                break;
            case "P":
                return "fa-tint"
                break;
            case "T":
                return "wi wi-thermometer"
                break;
            default:
                return "fa-plug"
                break;
        }
    };
}

function step_state() {
    return function (input) {
        switch (input.state) {
            case "I":
                return "";
                break;
            case "A":
                return "list-group-item-warning";
                break;
            case "D":
            default:
                return "list-group-item-info"
                break;
        }
    };
}

function hardware_name() {
    return function (input, data) {
        try {
            return data[input];
        }
        catch (err) {
            return "";
        }
    };
}

function kettle_name() {
    return function (input, data) {
        try {
            return data[input];
        }
        catch (err) {
            return "";
        }
    };
}


function switch_state2() {
    return function (state, states) {
        try {
            if (states[state]) {
                return "btn-success";
            }
            else {
                return "";
            }

        }
        catch (err) {
            return "";
        }
    }
}

function fermenter_state() {
    return function (id, state) {

        var key = "F" + id;

        if (state[key] == true) {
            return "btn-success";
        }
        else {
            return;
        }

    }
}

function hardware_state(CBPSwitch) {

    return function (input, type, data) {
        try {


            switch (type) {
                case 'A':
                    state = data[input.agitator]
                    break;
                case 'H':
                    state = data[input.heater]
                    break;
                case 'AUTO':
                    state = data[input.id].automatic
                    break;
                default:
                    state = data[input.id]
                    break
            }

            switch (state) {
                case true:

                    return "btn-success";
                    break;
                case false:

                    return "";
                    break;
            }
        }
        catch (err) {
            return "";
        }
    }
}


function get_temp() {
    return function (input, data) {
        try {
            return data[input];
        }
        catch
            (err) {
            return "";
        }
    }
}

function kettle_state() {
    return function (input, data) {
        for (i in data) {
            if (data[i].state == 'A' && data[i].kettleid == input.id) {
                return "panel-success";
            }
        }
    }
}

angular.module("cbpfilter", [])
    .filter("hardware_icon", hardware_icon)
    .filter("step_state", step_state)
    .filter("switch_state2", switch_state2)
    .filter("get_temp", get_temp)
    .filter("hardware_state", hardware_state)
    .filter("kettle_name", kettle_name)
    .filter("kettle_state", kettle_state)
    .filter("hardware_name", hardware_name)
    .filter("fermenter_state", fermenter_state);
