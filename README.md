## Open Data 500

The code behind the [Open Data 500][].

  [Open Data 500]: http://opendata500.com/us/

#### Installation

First, fork and clone this repo.

Next, you'll need the [Heroku Toolbelt][].

  [Heroku Toolbelt]: https://toolbelt.heroku.com/

In order to run locally, you'll need to pull down the env variables from the
Heroku remote (you can obtain the URL for the remote on Heroku's settings
page):

    git remote add heroku <heroku remote URL>
    heroku config --shell > .env

If you don't have access to an existing Heroku deployment, you'll need to
configure the following variables in a `.env` file:

    COOKIE_SECRET=
    MONGOLAB_URI=
    PAPERTRAIL_API_TOKEN=
    S3_BUCKET_NAME=
    TZ=

To run the server, you'll also need Python 2.7.x.  Inside a virtualenv:

    pip install -r requirements.txt

Use Foreman to start.  The site should be available [on port 5000][].

  [on port 5000]: http://localhost:5000

   Heroku local web

#### Development

If you make styling changes, you'll need to install the Ruby gem `sass`.

    gem install sass

Then, as you develop, you need to make sure to watch the css directory to
re-compile on the fly:

    sass --watch static/css
