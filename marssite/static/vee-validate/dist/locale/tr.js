!function(a,e){"object"==typeof exports&&"undefined"!=typeof module?module.exports=e():"function"==typeof define&&define.amd?define(e):(a.__vee_validate_locale__tr=a.__vee_validate_locale__tr||{},a.__vee_validate_locale__tr.js=e())}(this,function(){"use strict";var a={name:"tr",messages:{after:function(a,e){return a+" "+e[0]+" alanından ileri bir tarih olmalıdır."},alpha_dash:function(a){return a+" alanı harf ve tire (-) yada alttan tire (_) içerebilir."},alpha_num:function(a){return a+" yalnızca harf ve rakam içerebilir."},alpha_spaces:function(a){return a+" yalnızca harf boşluk (space) içerebilir."},alpha:function(a){return a+" yalnızca harf içerebilir."},before:function(a,e){return a+" "+e[0]+" alanından önce bir tarih olmalıdır."},between:function(a,e){return a+" "+e[0]+" ile "+e[1]+" aralığında olmalıdır."},confirmed:function(a){return a+" doğrulaması hatalı."},credit_card:function(a){return a+" numarası hatalı."},date_between:function(a,e){return a+" "+e[0]+" ile "+e[1]+" tarihleri arasında olmalıdır."},date_format:function(a,e){return a+" "+e[0]+" formatında olmalıdır."},decimal:function(a,e){void 0===e&&(e=["*"]);var r=e[0];return a+" sayısal"+("*"!==r?"ve noktadan sonra "+r+" basamaklı":"")+" olmalıdır."},digits:function(a,e){return a+" sayısal ve en fazla "+e[0]+" basamaklı olmalıdır."},dimensions:function(a,e){return a+" alanı "+e[0]+" piksel ile "+e[1]+" piksel arasında olmalıdır."},email:function(a){return a+" alanının geçerli bir e-posta olması gerekir."},ext:function(a){return a+" alanı geçerli bir dosya olmalıdır."},image:function(a){return a+" alanı resim dosyası olmalıdır."},in:function(a){return a+" alanına geçerli bir değer giriniz."},ip:function(a){return a+" alanı geçerli bir ip adresi olmalıdır."},max:function(a,e){return a+" alanı "+e[0]+" karakterden fazla olmamalıdır."},max_value:function(a,e){return a+" alanı "+e[0]+" yada daha az bir değer olmalıdır."},mimes:function(a){return a+" geçerli bir dosya olmalıdır."},min:function(a,e){return a+" alanına en az "+e[0]+" karakter girilmelidir."},min_value:function(a,e){return a+" alanı "+e[0]+" yada daha fazla bir değer olmalıdır."},not_in:function(a){return a+" alanına geçerli bir değer giriniz."},numeric:function(a){return a+" alanına sayısal bir değer giriniz."},regex:function(a){return a+" formatı geçersiz."},required:function(a){return a+" alanı gereklidir."},size:function(a,e){return a+" alanı "+e[0]+" KB'dan daha az olmalıdır."},url:function(a){return a+" geçersiz URL."}},attributes:{}};return"undefined"!=typeof VeeValidate&&VeeValidate&&(VeeValidate.Validator,!0)&&VeeValidate.Validator.addLocale(a),a});