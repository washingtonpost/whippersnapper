# Unnamed screenshot tool

Creates static, "backup" images for the Internet.

## Technical overview

This tool relies on [depict](https://github.com/kevinschaul/depict)
for taking screenshots.

## Installation (these are rough instructions)

    # Install depict
    npm install -g depict

    # Install python dependencies
    mkvirtualenv elections-screenshot-tool
    pip install -r requirements.txt

    # Set up configuration
    cp config.yaml.template config.yaml
    # Add AWS keys to config.yaml
    vim config.yaml

## Usage

    python elections_screenshotter/elections_screenshotter.py CONFIG_PATH

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

    - **page_load_delay** - Number

     Optional. Can be set on a global basis or per target.

    - **wait_for_js_signal** - Boolean

     Optional. Can be set on a global basis or per target.

- **local_image_directory**

  Required. Local directory to store images in.

- **aws_bucket**

  Required. Amazon S3 bucket to store the images in. Full path on AWS
  will be `<aws_bucket>/<aws_subpath>`.

- **aws_subpath**

  Required. The rest of the Amazon S3 path to store the images in. Full
  path on AWS will be `<aws_bucket>/<aws_subpath>`.

- **aws_access_key**

  Required. Access key credential for Amazon S3.

- **aws_secret_key**

  Required. Secret key credential for Amazon S3.

- **log_file** - String

  Optional. Defaults to `/var/log/unnamed-screenshot-tool-log.txt`. Path to a file to store logging information in.

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
