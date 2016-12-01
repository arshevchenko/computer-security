'use strict'
const Steganography = require("./lib/stegan");
const fs = require("fs");

var ciph = new Steganography();
var hide_text = fs.readFileSync(process.argv[2]).toString(),
    container_text = fs.readFileSync(process.argv[3]).toString();

ciph.hide(hide_text);

var enc = ciph.encode(container_text);
fs.writeFile("enc.txt", enc, function(err){
  if(err){
    return console.err(err);
  }
});

fs.readFile("enc.txt", "utf8", function(err, data){
  var dec = ciph.decode(data);

  fs.writeFile("dec.txt", dec, function(err){
    if(err){
      return console.err(err);
    }
  });
});
