'use strict'
const Steganography = require("./lib/steganography");
const fs = require("fs");

var ciph = new Steganography();
var hide_text = fs.readFileSync(process.argv[2]).toString();

ciph.hide(hide_text);

if(process.argv[3] == "--encode"){
  fs.readFile(process.argv[4], "utf8", function(err, data){
    var enc = ciph.encode(data);

    fs.writeFile("enc.txt", enc, function(err){
      if(err){
        return console.err(err);
      }
    });
  });
}else if(process.argv[3] == "--decode") {
  fs.readFile(process.argv[4], "utf8", function(err, enc_data){
    var dec = ciph.decode(enc_data);
    fs.writeFile("dec.txt", dec, function(err){
      if(err){
        return console.err(err);
      }
    });
  });
}
