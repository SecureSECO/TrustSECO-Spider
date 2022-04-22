const pynode = require('@fridgerator/pynode');
pynode.startInterpreter();

pynode.appendSysPath('env/Lib/site-packages');
pynode.appendSysPath('./');

pynode.openFile('controller');

function get_data(json_input, callback) {
    pynode.call('get_data', json_input, callback)
}

function update_tokens(github_token, libraries_token, callback) {
    pynode.call('update_tokens', github_token, libraries_token, callback)
}

exports.get_data = get_data;
exports.update_tokens = update_tokens;
