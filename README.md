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

### Extensions, Tools, and Plugins, oh my

* Flask-SQLAlchemy + geoalchemy2 + Flask-Migrate (+ Flask-Script)
  * _Experience_: **Entry to Intermediate**

    I have significant experience interfacing with ORM models, enabling a quick understanding of these tools, though specifically I have not used either.

  These tools were vital to interacting with the PostgreSQL+PostGIS table with abstracted ORMs.  Flask-Migrate (and its dependency Flask-Script) automated the entire database maintenance during development.  During the course of development, over 15 changes were made to the structure of the table, which were all handled seemlessly (almost) using the command line database scripting built-in, allowing less time on DB maintenance and more on code.  Additionally, these tools allowed the publication of the entire app's database to a remote server trivial via Fabric.

  ***Would do differently***: With more time, I would have contributed, or modified, Flask-Migrate to support geoalchemy2 fields.  As it is, each revision had to be made aware of necessary PostGIS index tables and fields.

* Fabric
  * _Experience_: **Entry to Intermediate**

    I have used this tool a number of times for personal projects, paired with Puppet, and have self-initiated learning, but very little professional experience so far.

  This tool automates 95% of the production server configuration including: package maintenance, python plugins, database installation setup; configuration; and data import, and server code synchronization with the [remote repository](http://github.com/joegilley/foodtruck-o-matic)

  ***Would do differently***: With more time, the other 5% of the server configuration can be automated.  Additionally, there are a number of areas of the application's code that could be improved with more modular settings between environments.



