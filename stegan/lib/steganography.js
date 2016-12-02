module.exports =
  class Steganography {

    constructor(name){
      this.bitArray = require("node-bitarray");
      this.bit_text = [];
    }

    hide(text){
      for(var i = 0; i < text.length - 1; i++){
        var element = this.bitArray.parse(text[i].charCodeAt(0)).reverse();
        while(element.length < 11)
          element.push(0);
          this.bit_text = this.bit_text.concat(element.reverse());
      }
    }

    encode(text){
      var text_container = text.split(" "),
          result_container = "";
      if(text_container.length - 1 < this.bit_text.length){
          console.log("Данный текст не может быть использовать в качестве контейнера.");
      }else{
        for(var i = 0; i < text_container.length; i++)
          if(this.bit_text[i] == 1 && i < this.bit_text.length)
            result_container += text_container[i] + "  ";
          else
            result_container += text_container[i] + " ";
      }

      return result_container;
    }

    decode(text){
      var char_decode = [],
          message = "";

      for(var i = 0; i < text.length; i++){
        if(text[i] == " " && text[i + 1] == " "){
          char_decode.push(1);
          i++;
        }else if (text[i] == " ") {
          char_decode.push(0);
        }

        if(char_decode.length == 11){
          message += String.fromCharCode(this.bitArray.toNumber(char_decode.reverse()));
          char_decode = [];
        }
      }

      return message;
    }
}
