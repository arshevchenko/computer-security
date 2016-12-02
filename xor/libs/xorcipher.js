module.exports =
  class XORCipher{

    constructor(secret_key){
      this.key = secret_key;
    }

    code(message){
      var ch = message.toLowerCase();
      var result = "", len;

      for (var i = 0, j = 0; i < ch.length; i++, j++){
        if (ch[i] >= 'а' && ch[i] <= 'я' || ch[i] >= '0' && ch[i] <= '9'
            || ch[i] == '.' || ch[i] == ',' || ch[i] == '!' || ch[i] == '?'
            || ch[i] == '—' || ch[i] == '-' || ch[i] == ':' || ch[i] == ';'
            || ch[i] == '(' || ch[i] == ')' || ch[i] == '{' || ch[i] == '}'
            || ch[i] == '[' || ch[i] == ']' || ch[i] == '<' || ch[i] == '>'
            || ch[i] == '\"' || ch[i] == '\'' || ch[i] == '\ ' || ch[i] == '&'
            || ch[i] == '*'  || ch[i] == '\n' || ch[i] == '\f') {
          result += String.fromCharCode(ch[i].charCodeAt(0) ^ this.key);
        }else{
          console.log("Ошибка! Символ " + ch[i].charCodeAt(0) + " не разрешен. Остановка шифрования.");
          break;
        }
      }

      return result;
    }
}
