const globals_NS = {}


globals_NS.datetimeToTimeString = function (obj) {
    let dateObj = new Date(obj);
    return dateObj.toLocaleTimeString('en-GB').split(":")[0] + ":" + dateObj.toLocaleTimeString().split(":")[1];
};