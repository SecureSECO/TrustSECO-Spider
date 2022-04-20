// if this module can use trustfacts functions an external file sould also be able to(i think)
const trustfacts = require('./trustfacts')

trustfacts.gh_get_gitstar_ranking('numpy', 'numpy', (err,result) => {console.log(result)})