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
