'use strict'
const fs = require("fs");
var XORCipher = require("./libs/xorcipher");

var data = fs.readFileSync(process.argv[2])
             .toString()
             .replace("\f", "");

var xor = new XORCipher(6),
    encode = xor.code(data),
    decode = xor.code(encode);

fs.writeFile(process.argv[3], encode, function(err){
  if(err){
    return console.err(err);
  }
});
