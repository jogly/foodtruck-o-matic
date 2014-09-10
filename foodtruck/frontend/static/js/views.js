
ft.GoogleMapView = Backbone.View.extend({
  el: '.map-container',
  initialize: function(options) {
    // Add the 'this' context to our method `add`
    _.bindAll(this, 'add', 'remove', 'select', '_show_infoWindow');

    this.collection = options.collection
    this.collection.each(this.add)
    this.collection.bind('add', this.add)
    this.collection.bind('remove', this.remove)
    this.collection.on('select', this.select)

    // Nothing to do yet, but hold onto a `InfoWindow` for later
    this._infoWindow = new google.maps.InfoWindow({
      // content: '<button type="button" class="btn btn-default btn-sm"><span class="glyphicon glyphicon-remove"></span></button>'
      content: 'oops'
    });
    // A map of id to marker to remove them when done
    this._markers = {}
    this.render();
  },
  add: function(model) {
    // Create a map marker for this model!
    var marker = new google.maps.Marker({
      position: new google.maps.LatLng(
        model.get('latitude'),
        model.get('longitude')),
      map: this._map,
      title: model.get('applicant')
    });

    model._marker = marker

    google.maps.event.addListener(marker, 'click', function() {
      this._show_infoWindow(model)
    }.bind(this));
  },
  remove: function(model) {
    model._marker.setMap(null);
  },
  select: function(model) {
    this._map.panTo(model._marker.getPosition());
    this._show_infoWindow(model)
  },
  render: function() {
    // Center and zoom the map onto an arbitrary location in SF
    var mapOptions = {
      center: new google.maps.LatLng(37.7841781516735, -122.394064145441),
      zoom: 14
    };
    // Put the map there!
    this._map = new google.maps.Map(this.el, mapOptions);
  },
  _show_infoWindow: function(model) {
    this._infoWindow.open(this._map, model._marker)
    this._infoWindow.setContent(_.template($('#template-foodtruck').html())(model.attributes));
  }
});

ft.FoodtruckView = Backbone.View.extend({
  el: 'li.foodtruck',
  initialize: function(options) {
    this._model = options.model;
    this.el = '#ft-'+this._model.id
    $(this.id).bind('click', this.select)
  },
  render: function() {
    return _.template($('#template-foodtruck').html())(this._model.attributes);
  }
});

ft.AddressSearchView = Backbone.View.extend({
  el: '#address-search',
  events: {
    'click button' : 'submit',
    'keypress input' : 'enterShortcut'
  },
  initialize: function(options) {
    _.bindAll(this, 'submit', 'enterShortcut')
    this.collection = options.collection
  },
  submit: function(e) {
    $(e.currentTarget).addClass('disabled')
    var address = $('#address-search-bar').val()
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode({
      address: address,
      region: 'en'
    }, function(results, status) {
      $(e.currentTarget).removeClass('disabled')
      if (status == google.maps.GeocoderStatus.OK) {
        this.collection.coords = {
          latitude: results[0].geometry.location.lat(),
          longitude: results[0].geometry.location.lng()
        };
        this.collection.fetch().done(function() {

        });
      } else {
        console.log('errorrrr')
      }
    }.bind(this));
  },
  enterShortcut: function(e) {
    if (e.which === 13) {
      this.submit(e);
    }
  }
});

ft.FoodtrucksView = Backbone.View.extend({
  el: '.foodtrucks-list',
  events: {
    'click li' : 'select'
  },
  initialize: function(options) {
    _.bindAll(this, 'add', 'select');
    this._model_views = [];
    this.collection = options.collection;
    // If there are already entries in the collection
    this.collection.each(this.add);
    // Watch for changes to the collection!
    this.collection.bind('add', this.add);
    this.collection.bind('remove', this.remove);
  },
  add: function(model) {
    var modelView = new ft.FoodtruckView({
      model: model
    });
    model._view = modelView
    this.$el.append(modelView.render())
  },
  remove: function(model) {
    $(model._view.el).remove()
    model._view.remove()
    model._view = null
  },
  select: function(e) {
    var id = $(e.currentTarget).data('id')
    $('li.foodtruck').removeClass('selected')
    $(e.currentTarget).addClass('selected')
    this.collection.trigger('select', this.collection.get(id))
  }
});
