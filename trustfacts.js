const pynode = require('@fridgerator/pynode');
pynode.startInterpreter();

pynode.appendSysPath('env/Lib/site-packages');
pynode.appendSysPath('./');

pynode.openFile('controller');

function get_data(json_input, callback) {
    pynode.call('get_data', json_input, callback)
}

exports.get_data = get_data;
