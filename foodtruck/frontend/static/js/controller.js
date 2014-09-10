$(document).ready(function(){
  // Get our data source
  var foodtrucks = new ft.Foodtrucks();

  // Get our map view, and connect point it to the data source.
  // The view will take care of registering itself
  var googMapView = new ft.GoogleMapView({
    collection: foodtrucks
  });

  // Same for the sidebar foodtruck list view
  var foodtrucksView = new ft.FoodtrucksView({
    collection: foodtrucks
  });

  // Do we have geolocation data?
  if ("geolocation" in navigator) {
    console.log('we got you!');
    navigator.geolocation.getCurrentPosition(function(position) {
      console.log('got a lock on ya too')
      foodtrucks.coords = position.coords
      foodtrucks.fetch();
    });
  } else {
    console.log('you\'re off the radar :T');
      // Start us off with an API call!
    foodtrucks.fetch({
      error: function(error) {
        console.log(error)
      }
    });
  }
});
