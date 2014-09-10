
ft.GoogleMapView = Backbone.View.extend({
  el: '.map-container',

  initialize: function(options) {
    // Add the 'this' context to our method `add`
    _.bindAll(this, 'add', 'remove');

    this.collection = options.collection
    this.collection.each(this.add)
    this.collection.bind('add', this.add)
    this.collection.bind('remove', this.remove)

    // Nothing to do yet, but hold onto a `InfoWindow` for later
    this._infoWindow = new google.maps.InfoWindow({
      // content: '<button type="button" class="btn btn-default btn-sm"><span class="glyphicon glyphicon-remove"></span></button>'
      content: 'oh'
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

    var view = this
    google.maps.event.addListener(marker, 'click', function() {
      view._infoWindow.open(view._map, marker);
    });

    model._marker = marker
  },

  remove: function(model) {
    model._marker.setMap(null)
  },

  render: function() {
    // Center and zoom the map onto an arbitrary location in SF
    var mapOptions = {
      center: new google.maps.LatLng(37.7841781516735, -122.394064145441),
      zoom: 14
    };
    // Put the map there!
    this._map = new google.maps.Map(this.el, mapOptions);
  }
});

ft.FoodtruckView = Backbone.View.extend({
  el: 'li',
  className: 'foodtruck',
  initialize: function(options) {
    this._model = options.model;
    this.id = this._model.id
  },
  render: function() {
    return _.template($('#template-foodtruck').html())(this._model.attributes);
  }
});

ft.FoodtrucksView = Backbone.View.extend({
  el: '.foodtrucks-list',

  initialize: function(options) {
    _.bindAll(this, "add");
    this._model_views = [];
    this.collection = options.collection;
    // If there are already entries in the collection
    this.collection.each(this.add);
    // Watch for changes to the collection!
    this.collection.bind('add', this.add)
  },
  add: function(model) {
    var modelView = new ft.FoodtruckView({
      model: model
    });
    model._view = modelView
    this.$el.append(modelView.render())
  },
  remove: function(model) {
    $('li#'+model.id).remove()
    model._view = null
  }
});
