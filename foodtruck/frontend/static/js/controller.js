$(document).ready(function(){
  // This is the model that takes the lat,lngs from the goog.
  var coordModel = new ft.AddressResult();

  // This is one of the major drivers for this application.
  // Changes to this collection update the map and the foodtruck list views
  var foodtrucks = new ft.Foodtrucks(null, {
    coordModel: coordModel
  });

  // Get our map view, and connect it to the data source.
  // The view will take care of registering itself
  var googMapView = new ft.GoogleMapView({
    collection: foodtrucks
  });
  // // We'll render this now
  googMapView.render();

  // // Same for the sidebar foodtruck list view
  var foodtrucksView = new ft.FoodtrucksView({
    collection: foodtrucks
  });

  // The search view only needs its SearchResults model
  var searchView = new ft.AddressSearchView({
    model: foodtrucks
  });

  // Do we have geolocation data?
  if ("geolocation" in navigator) {
    console.log('We know that you have geolocation information on you!');
    navigator.geolocation.getCurrentPosition(function(position) {
      console.log('got a lock on ya too')
      coordModel.set({
        latitude: position.coords.latitude,
        longitude: position.coords.longitude
      });
    });
  } else {
    console.log('you\'re off the radar :T');
      // Start us off with an API call!
    coordModel.trigger('change');
  }
});
