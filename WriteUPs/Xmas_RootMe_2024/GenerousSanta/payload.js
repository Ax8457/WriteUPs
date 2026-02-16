const mongoose = require('/usr/app/node_modules/mongoose');
const fs = require('fs');
let flagContent = fs.readFileSync('../../flag.txt', 'utf8');
const flagSchema = new mongoose.Schema({
    name: { type: String, default: 'Flag' },
    description: { 
        type: String, 
        default: flagContent,
        set: (value) => value.startsWith('Description of') ? flagContent : value
    }
});
flagSchema.methods.store = function() {
    console.log('Flag !!!!!!!!');
    return this;
};
module.exports = mongoose.model('xmasflag', flagSchema);
