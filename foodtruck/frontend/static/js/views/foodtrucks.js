ft.FoodtrucksView = Backbone.View.extend({
  el: '.foodtrucks-list',
  events: {
    'click li' : 'itemClicked'
  },
  initialize: function(options) {
    _.bindAll(this, 'add', 'select', 'itemClicked');
    this._model_views = [];
    this.collection = options.collection;
    // If there are already entries in the collection
    this.collection.each(this.add);
    // Watch for changes to the collection!
    this.listenTo(this.collection, 'add', this.add);
    this.listenTo(this.collection, 'remove', this.remove);
    this.listenTo(this.collection, 'change:selection', this.select);
    // Hash to hold the sub views
    this._modelViews = {};
  },
  add: function(model) {
    var modelView = new ft.FoodtruckView({
      model: model
    });
    this.$el.append(modelView.render())

    this._modelViews[model.id] = modelView;
  },
  remove: function(model) {
    $(this._modelViews[model.id].el).remove();
    this._modelViews[model.id].remove();
    this._modelViews[model.id] = null;
    delete this._modelViews[model.id];
  },
  select: function(model) {
    $('li.foodtruck').removeClass('selected');
    $(this._modelViews[model.id].el).addClass('selected');
  },
  itemClicked: function(e) {
    var id = $(e.currentTarget).data('id');
    this.collection.trigger('change:selection', this.collection.get(id));
  }
});
