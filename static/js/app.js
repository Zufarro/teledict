(function(window) {
  window.onload = function() {
    var app = new Vue({
      el: '#app',
      data: {
        logo: "Translater-dictionary",
        "word": "",
        "language": "en_ru",
        translate: "",
        "word_to_add": "",
        result_add_word: "",
        "word_of_added_translation": "",
        "translation_to_add": "",
        result_add_translation: "",
      },
      methods: {
        getTranslate: function () {
          var self = this;
          var form = {
            "word": this.word,
            "language": this.language
          };
          console.log(form);
          axios.post("/translate", form).then(function(resp) {
              console.log(resp);
              data = resp.data;
              self.translate = "Перевод: "+data;
            });
        },
        addWord: function () {
          var self = this;
          var form = {
            /*"language": this.language,*/
            "add_word": this.add_word
          };
          axios.post("/words", form).then(function(resp) {
              data = resp.data;
              self.result_add_word = data;
            });
        },
        addTranslation: function () {
          var self = this;
          var form = {
            "language": this.language,
            "word_of_added_translation": this.word_of_added_translation,
            "translation_to_add": this.translation_to_add
          };
          console.log(form);
          axios.post("/translation", form).then(function(resp) {
              data = resp.data;
              self.result_add_translation = data;
            });
        }
      },
    });
  };

}(window))
