const pynode = require('@fridgerator/pynode');
pynode.startInterpreter();

pynode.appendSysPath('src/env/Lib/site-packages');
pynode.appendSysPath('src');

pynode.openFile('interface');

pynode.call('testfunc', 4, (err, result) => {
   console.log(result);
});

function gh_get_contributor_count(imput, callback){
    pynode.call('testfunc',imput, callback)
}

export function gh_get_contributor_count();

// Cosy
gh_get_contributor_count('numpy', (error, result) => {
    
});
