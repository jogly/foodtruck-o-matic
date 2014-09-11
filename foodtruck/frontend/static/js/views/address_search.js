// The view that contains the logic for what to do with the search bar.
// This view registers events against its sub-elements, clicking the button,
// and keypresses check for the enter key.
// Instantiate this view with an AddressResult instance

ft.AddressSearchView = Backbone.View.extend({
  el: '#address-search',
  events: {
    'click button' : 'submit',
    'keypress input' : 'enterShortcut'
  },
  initialize: function(options) {
    _.bindAll(this, 'submit', 'enterShortcut');
    this.result = options.model;

    this.$button = this.$el.find('button');
    this.$searchbar = this.$el.find('input[type="text"]');
    this.geocoder = new google.maps.Geocoder();
  },
  submit: function(e) {
    // Let's not let them do that again for a little bit
    // (until the request finishes)
    this.disable();

    var address = this.$searchbar.val();

    this.geocoder.geocode({
      address: address,
      region: 'en'
    }, function(results, status) {
      this.enable()
      if (status == google.maps.GeocoderStatus.OK) {
        this.result.set({
          latitude: results[0].geometry.location.lat(),
          longitude: results[0].geometry.location.lng()
        });
      } else {
        console.log('this is not a helpful errorrrr');
      }
    }.bind(this));
  },
  enterShortcut: function(e) {
    if (e.which === 13 && !this.isDisabled) {
      this.submit(e);
    }
  },
  disable: function() {
    this.$button.addClass('disabled');
    this.isDisabled = true;
  },
  enable: function() {
    this.$button.removeClass('disabled');
    this.isDisabled = false;
  }
});
