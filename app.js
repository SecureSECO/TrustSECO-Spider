// if this module can use trustfacts functions an external file sould also be able to(i)
const trustfacts = require('./trustfacts')

trustfacts.testFunc(4, (err,result) => {console.log(result)})