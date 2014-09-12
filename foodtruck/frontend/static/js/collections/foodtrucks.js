// This model contains all of the foodtruck models that will populate the app.
// Changes to the passed coordsModel will trigger a renewal of the list

ft.Foodtrucks = Backbone.Collection.extend({
  model: ft.Foodtruck,
  url: function() {
    if (this.coordModel) {
      return '/api/foodtrucks/nearby?latitude='+this.coordModel.get('latitude')
              +'&longitude='+this.coordModel.get('longitude')+'&per_page=10';
    }
    // Default to the full list.  Shouldn't happen
    return 'api/foodtrucks';
  },
  parse: function(response) {
    // I don't know why collections assume the result will be a top-level
    // array, that is unsafe.
    // We'll parse the result set from the top-level object
    return response.foodtrucks;
  },
  initialize: function(models, options) {
    this.listenTo(this, 'add', function(e) {
      console.log('added something');
    });
    _.bindAll(this, 'coordsChanged');
    this.coordModel = options.coordModel;
    this.listenTo(this.coordModel, 'change', this.coordsChanged);
  },
  coordsChanged: function() {
    // Remove all of the existing entries.  We want to maintain the order of
    // the results from the server. Using fetch will intelligently update items,
    // so if we have two separate queries, with an overlapping data set,
    // 'remove' will be fired for some but the union set will bubble to the top
    //of the list. This is incorrect, so we start fresh.  We could use
    //``reset()`` but that only fires the one 'reset' event and our set is not
    //large.
    // If the API supported a distance field, we could use a custom comparator
    //and this would be more efficient
    var self = this;
    this.set();
    this.fetch({
      error: function(col, res, opt) {
        console.log('Error fetching foodtrucks: %o', res);
      },
      success: function(col, res, opt) {
        col.trigger('done');
      }
    })
  }
});
