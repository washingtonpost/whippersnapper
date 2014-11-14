# Whippersnapper

Whippersnapper is an automated screenshot tool to keep a visual history
of content on the web.

The concept for Whippersnapper first came up as a last-ditch backup system
for the Washington Post's live election results maps. Election nights
are notoriously volatile for news organizations, so we planned to store
static image versions of our results maps throughout the night in case
the need for a fallback arose.

## Technical overview

This tool relies on [depict](https://github.com/kevinschaul/depict)
for taking screenshots.

## Installation (these are rough instructions)

    # Install depict
    npm install -g depict

    # Install python dependencies
    mkvirtualenv whippersnapper
    pip install -r requirements.txt

    # Set up configuration
    cp config.yaml.template config.yaml
    # Add AWS keys to config.yaml
    vim config.yaml

## Usage

    python whippersnapper/whippersnapper.py CONFIG_PATH

## Config file options

- **targets** - List of target suboptions

  Required. A list of images to include. Each item in this list can
  include these suboptions:

    - **slug** - String

      Required. Used to name the image files.

    - **url**

      Required. The URL of the page you are screenshotting.

    - **selector** - String

      Optional. Defaults to `body`. The selector of the element you wish
      to screenshot.

    The following options can override the global options on a
    per-target basis:

    - **page_load_delay**
    - **wait_for_js_signal**
    - **local_image_directory**
    - **aws_subpath**
    - **override_css_file**
    - **failure_timeout**

- **local_image_directory**

  Required. Local directory to store images in.

- **skip_upload**

  Optional. Default: false. Whether to skip the upload process.

- **aws_bucket**

  Required (unless `skip_upload` is true). Amazon S3 bucket to store the
  images in. Full path on AWS will be `<aws_bucket>/<aws_subpath>`.

- **aws_subpath**

  Required (unless `skip_upload` is true). The rest of the Amazon S3
  path to store the images in. Full path on AWS will be
  `<aws_bucket>/<aws_subpath>`.

- **aws_access_key**

  Required (unless `skip_upload` is true). Access key credential for Amazon S3.

- **aws_secret_key**

  Required (unless `skip_upload` is true). Secret key credential for Amazon S3.

- **log_file** - String

  Optional. Default: `$(pwd)/screenshotter.log` Path to a file to store
  logging information in.

- **delete_local_images**

  Optional. Default: false. Whether to delete the local images after
  uploading them to Amazon S3.

- **time_between_screenshots** - Number

  Optional. Default: `60`. Seconds to wait between taking screenshots

- **override_css_file**

  Optional. Path to a CSS file that overrides any existing styles on the
  page. Useful when screenshotting a page that you cannot or do not want
  to modify.

- **page_load_delay** - Number

  Optional. Default: `2`. Seconds to wait after the page is loaded, to
  ensure that any JavaScript has finished running.

- **wait_for_js_signal** - Boolean

  Optional. Default: `false`. Instruct depict to wait for the target
  page's JavaScript to call the function `window.callPhantom()`. This
  may be used to wait for an amount of JavaScript to execute instead of
  the option `page_load_delay`, which waits an amount of time.

- **failure_timeout** - Number

  Optional. Default: `30`. The maximum number of seconds the browser
  remains open. If PhantomJS can't open the page or something hangs up,
  this will kill the process. For no time limit, set `failure_timeout`
  to `0`.
