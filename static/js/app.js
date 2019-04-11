(function(window) {
  window.onload = function() {
    var app = new Vue({
      el: '#app',
      data: {
        "translations": [],
        "words": [],
        "logo": "Translater-dictionary",
        "word": "",
        "lang": "en",
        "transl": "ru",
        "translation": "",
        "new_word": "",
        "result_new_word": "",
        "word_to_translate": "",
        "new_translation": "",
        "result_new_translation": "",
      },
      methods: {
        getTranslate: function () {
          var self = this;
          var form = {
            "word": this.word
          };
          console.log(form);
          axios.post("/translate/" + this.lang + "/" + this.transl, form).then(function(resp) {
              data = resp.data;
              self.translation = "Перевод: "+data;
          });
        },
        addWord: function () {
          var self = this;
          var form = {
            "word": this.new_word
          };
          axios.post("/words/" + this.lang, form).then(function(resp) {
              data = resp.data;
              self.result_new_word = data;
          });
        },
        addTranslation: function () {
          var self = this;
          var form = {
            "word": this.word_to_translate,
            "translation": this.new_translation
          };
          console.log(form);
          axios.post("/translation/" + this.lang + "/" + this.transl, form).then(function(resp) {
              data = resp.data;
              self.result_new_translation = data;
          });
        },
        refreshTable: function() {
          var self = this;
          axios.get("/translation/" + this.lang + "/" + this.transl).then(function(resp) {
            console.log(resp.data);
            self.translations = resp.data;
          });
        },
        refreshWords: function() {
          var self = this;
          axios.get("/words/" + this.lang).then(function(resp) {
            console.log(resp.data);
            self.words = resp.data;
          });
        }
      },
      mounted: function() {
        console.log("app loaded!");
        this.refreshTable();
        this.refreshWords();
      }
    });
  };

}(window))
