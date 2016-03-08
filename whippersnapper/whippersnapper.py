#!/usr/bin/env python

import logging
import os
import subprocess
import sys
import time
import inspect

import yaml

import screenshotter
import uploader

class WhipperSnapper(object):
    """
    Implements all screenshot-related logic.
    """

    def __init__(self):
        if len(sys.argv) != 2:
            self.usage()
            sys.exit(1)

        config_filepath = sys.argv[1]
        self.config = self.load_config(config_filepath)
        self.log_file = self.init_logging()
        self.screenshotter = screenshotter.Screenshotter(self.config)
        if not self.config.get('skip_upload'):
            self.uploader = uploader.Uploader(self.config)

    def main(self):
        """
        Runs through the full screenshot process.
        """

        print """
Whippersnapper is running. To view its log file:

    tail -f %s

To quit, press ^C (ctrl-C).""" % (self.log_file)

        while True:
            targets = self.screenshotter.take_screenshots()
            if hasattr(self, 'uploader'):
                self.uploader.upload_screenshots(targets)
                # TODO Image delete code probably doesn't belong here
                if (self.config.get('delete_local_images')):
                    [os.remove(path.get('local_filepath')) for path in targets]
            time.sleep(self.config.get('time_between_screenshots'))

    def init_logging(self):
        """
        Create a log file, and attach a basic logger to it.
        """
        log_file = os.path.abspath(os.path.expanduser(self.config.get('log_file')))
        # Create the log file if it does not yet exist
        with open(log_file, 'a+'):
            pass
        logging.basicConfig(filename=log_file,
                format='%(levelname)s:%(asctime)s %(message)s',
                level=logging.INFO)
        return log_file

    def load_config(self, config_filepath):
        """
        Load configuration from config.yaml.

        Many options have defaults; use these unless they are overwritten in
        config.yaml. This file includes the urls, css selectors and slugs for
        the targets to screenshot.
        """

        log_file = os.path.abspath(os.path.expanduser(os.path.dirname(
                os.path.abspath(__file__)) + '/../whippersnapper.log'))

        config = {
            'skip_upload': False,
            'aws_bucket': '',
            'aws_subpath': '',
            'aws_access_key': None,
            'aws_secret_key': None,
            'log_file': log_file,
            'delete_local_images': False,
            'time_between_screenshots': 60,
            'hide_selector': ' ',
            'override_css_file': None,
            'page_load_delay': 2,
            'browser_width': 1440,
            'wait_for_js_signal': False,
            'failure_timeout': 30,
        }

        required = (
            'targets',
            'local_image_directory',
        )

        raw_config = None

        with open(config_filepath) as f:
            raw_config = yaml.load(f)

        for option_name, option_value in raw_config.iteritems():
            config[option_name] = option_value

        for option in required:
            try:
                config[option] = raw_config[option]
            except KeyError:
                raise RuntimeError('Config is missing required attribute: %s'
                        % option)

        return config

    def usage(self):
        config_template_file = 'https://raw.githubusercontent.com/washingtonpost/whippersnapper/master/config_templates/config.yaml.template'

        """
        Print usage information.
        """
        print """
        USAGE: whippersnapper CONFIG_FILEPATH

        To see an example config file:

        curl %s
        """ % config_template_file

def launch_new_instance():
    """
    Launch an instance of Whippersnapper.
    """
    try:
        s = WhipperSnapper()
        s.main()
    except KeyboardInterrupt:
        # Print a blank line
        print

if __name__ == '__main__':
    launch_new_instance()
