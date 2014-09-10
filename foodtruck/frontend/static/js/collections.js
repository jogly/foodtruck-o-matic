ft.Foodtrucks = Backbone.Collection.extend({
  model: ft.Foodtruck,
  url: function() {
    if (this.coords) {
      return '/api/foodtrucks/nearby?latitude='+this.coords.latitude+'&longitude='+this.coords.longitude+'&per_page=20';
    } else {
      return 'api/foodtrucks';
    }
  },
  parse: function(response) {
    return response.foodtrucks;
  }
});
