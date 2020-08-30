function min() {return Math.min.apply(null, arguments)}
function max() {return Math.max.apply(null, arguments)}
function abs(x) {return Math.abs(x)}
function isinstance(baseobj, obj) {return obj instanceof baseobj}
function len(obj) {
    if(getattr(obj, "length")) {
        return obj.length;
    } else {
        throw Error("Object " + obj + " does not have attribute 'length'");
    }
}
function getattr() {
    var obj = arguments[0];
    var attr = arguments[1];
    var defval = arguments.length > 2 ? arguments[2] : null;
    if(obj[attr] === undefined) return defval;
    else return obj[attr];
}
function map(fn, iter) {
    for(var i = 0; i < iter.length; i++) {
        iter[i] = fn(iter[i]);
    }
    return iter;
}
function print() {
    var str = ""; 
    for(var i = 0; i < arguments.length; i++) {
        if((i + 1) === arguments.length) {
            str += arguments[i];
        } else {
            str += arguments[i] + " ";
        }
    }
    console.log(str);
}
function sum() {
    var s = arguments[0];
    for(var i = 1; i < arguments.length; i++){
        s += arguments[i];
    }
    return s;
}
function type(obj) {return typeof(obj)}
function zip(x, y) {
    var zipped = {};
    for(var i = 0; i < x.length; i++) {
        zipped[x[i]] = y[i];
    }
    return zipped;
}
function range() {
    if(arguments.length > 3) throw Error("Too many aguments to range(" + arguments + ")");
    var start = arguments[0] 
    var end = arguments[1]
    var step = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : 1;
    var iter = [];
    if(arguments.length === 1) {
        end = start;
        start = 0;
    }
    for(var i = start; i < end; i+=step) {
        iter.push(i);
    }
    return iter;
}

