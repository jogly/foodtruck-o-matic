# San Francisco's foodtruck-o-matic

## Foreword

This is a relatively simple back-end and front-end (**full-stack**) application as a demonstration of coding (or more aptly, learning) ability.  This application's front and back ends are completely logically separated by a REST API, as defined in this application's [back-end documentation](http://josephgilley.com/doc/).  The data was sourced in its entirety by San Francisco government's [OpenData API](https://data.sfgov.org/Economy-and-Community/Mobile-Food-Facility-Permit/rqzj-sfat).

## About

Hosted at http://josephgilley.com, this application presents the user with a simple single page application that will attempt to geolocate you using the browser's native [Geolocation API](http://dev.w3.org/geo/api/spec-source.html).  If this is unavailable, the application will load an arbitrary selection of foodtrucks by default.  Additionally, the user is presented with the ability to search for an address, which is geolocated by Google's [Geolocater JavaScript API](https://developers.google.com/maps/documentation/javascript/examples/map-geolocation), and will present the user with the closest foodtrucks.

## Technologies

### Back-end

* Language: Python
  * _Experience_: **Entry to Intermediate**

    My experience with Python is limited to self-initiated learning and on-line classes (such as Coursera's 'Data Science')

  This language was chosen for the back-end for multiple reasons.  Foremost, I wanted the practical experience of developing in the language that supports the major aspects of Uber's own back-end.  Additionally, this language provides an accelerated development cycle that is desirable for a quick turnaround project like this.  Furthermore, I am able to demonstrate my ability to quickly adapt to a new language and its idioms.

* Micro-framework: Flask
  * _Experience_: **Entry**

    This was my first foray into the magnificent framework that is Flask, and I am happier for it.

  This framework was chosen in part to satisfy the coding challenges suggestion.  However, the choice was made to use this micro-framework primarily because of the vast resources, extensions, and documentation that the community has developed, as well as the flexibility and ease of configuration in a production server.

  The Flask package's structure and code is documented and made available at http://josephgilley.com/doc/ by Sphinx (see below)

* Database: PostgreSQL (+PostGIS)
  * _Experience_:
    * _SQL_: **Intermediate to Advanced**

      I am very comfortable in a number of dialects of SQL, though PostgreSQL's is new.

    * _PostGIS_: **Entry**

      I am new to Geolocation tools, but learned an enormous amount from this project and am quickly becoming more comfortable understanding the PostGIS language, though I need to continue my own education on this technology.

  PostgreSQL+PostGIS is responsible for storing the data obtained from SF's Foodtruck API. Upon loading the information into the table, a `Geometry(POINT)` field is generated from the `latitude` and `longitude` values and is used by the appplication to source the `/foodtrucks/nearby` REST API call (completely scripted by Fabric, see below).  This allows crazy fast distance selection and sorting (`/foodtrucks/nearby` average <50ms for the entirety of each call)

* HTTP Server: NGINX (as reverse proxy, and as static file host)
  * _Experience_: **Entry**

    I am accustomed to very simple apache configurations, and the concepts of HTTP servers, including reverse proxies, however I have little system administration experience (and from long ago).

  NGINX provided the application with production quality HTTP reverse proxy-ing and static file hosting.  I chose NGINX over Apache primarily becaues I had never used it and wanted the experience of a slightly different server implementation.

  ***Would do differently***:

##### Security

    Due to my limited systems administration experience, very little security is currently implemented on the production server.  A basic security group is applied to the Amazon EC2 instance, and SSH is securely configured to only users with a valid private key.  Otherwise, there is very little protection against API abuse.

##### Scalability

    * No cacheing is currently being performed against API requests.  There **definitely** should be.  I would implement a Redis cache service, and cache requests locations.  If I want to be extra sneaky, I would cache locations that are very close together with the same key.  This would mean even **faster** response times and the ability to handle surges for specific address or areas very easily.
    * No cacheing is currently being performed against static files.  This was part of the initial plan for the project.  This would be simple to set up with Varnish.  I _just_ ran out of time for this piece.  This would be my next priority, since the API calls are fast enough, serving the same javascript files and css over and over is the next largest bottleneck.
* WSGI Server: Gunicorn
  * _Experience_: **Entry** _

    This was enormously simple to set up.  Very straightforward local hosting that NGINX forwards upstream to. It would be trivial to alter the NGINX configuration to facilitate a *horizontal scaling* architecture in which Gunicorn is listening on multiple machines (hopefully virtual) locally and NGINX load balances across them.

#### Extensions, Tools, and Plugins, oh my

* Flask-SQLAlchemy + geoalchemy2 + Flask-Migrate (+ Flask-Script)
  * _Experience_: **Entry to Intermediate**

    I have significant experience interfacing with Java ORM models, which facilitated a quick understanding of these tools, though specifically I have not used either.

  These tools were vital to interacting with the PostgreSQL+PostGIS table with abstracted ORMs.  Flask-Migrate (and its dependency Flask-Script) automated the entire database maintenance during development.  During the course of development, over 15 changes were made to the structure of the table, which were all handled seemlessly (almost) using the command line database scripting built-in, allowing less time on DB maintenance and more on code.  Additionally, these tools allowed the publication of the entire app's database to a remote server trivial via Fabric.

  ***Would do differently***: With more time, I would have contributed, or modified, Flask-Migrate to support geoalchemy2 fields.  As it is, each revision had to be made aware of necessary PostGIS index tables and fields, which was trivial but mundane.

* unittest + nose
  * _Experience_: **Entry to Intermediate** _I am accustomed to unit testing and these utilities, while new to me, followed many best practices that I am already familiar with._

  ***Would do differently:*** More exhaustive unit testing! Specifically I did not test for error responses, but I did test for successful responses.  Since the front-end, at this time, does not utilize the error responses (besides my own silliness during debugging), I deemed this a lower priority.

* Fabric
  * _Experience_: **Entry to Intermediate**

    I have used this tool a number of times for personal projects, paired with Puppet, and have self-initiated learning, but very little professional experience so far.

  This tool automates 95% of the production server configuration including: package maintenance, python plugins, database installation setup; configuration; and data import, and server code synchronization with the [remote repository](http://github.com/joegilley/foodtruck-o-matic)

  ***Would do differently***: With more time, the other 5% of the server configuration can be automated.  Additionally, there are a number of areas of the application's code that could be improved with more modular settings between environments.

* Sphinx

  Sphinx documentation is available at http://josephgilley.com/doc/
  * _Experience_: **Entry**

    A very flexible documentation processor, an understanding of other doc processors made the adoption trivial.

### Front-end

* Mostly JavaScript (also basic HTML5 and CSS3)
  * _Experience_: **Entry to Intermediate**.  _Tends towards Intermediate, but rustiness in the object model makes me humble_

  Being a single page app puts most of the work of interactivity and dynamism on scripting.  Pretty straightforward here.

* CSS Bootstrapped: **Intermediate** _Not too much this tech.  Include and use._

  http://getbootstrap.com

* MVC: Backbone.js
  * _Experience_: **Entry** _I am very familiar with the concepts of MVC, and the programming model that arises from its practice, so the adoption of this technology was trivial after climbing the learning curve and understanding a number of *gotchas*._

  ***Would do differently***:
    * With more time, I am certain that separation of some pieces of logic can be improved.  With the time constraints, I chose on seldom occasions to _cheat_ a little by generating model events from within a view.  I could also do with some signals from the `GoogleMapView` to the collections model to keep track of what is highlighted on the map (just a usability feature, reall).
    * And of course automate the front-end testing.


