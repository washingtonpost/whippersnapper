import datetime
import logging
import subprocess
import time

import pprint

import util

class Screenshotter(object):
    """
    Implements all screenshot-related logic.
    """

    def __init__(self, config):
        self.config = config
        self.screenshot_filenames = []

    def get_target_config(self, image):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.config)
        pp.pprint(image)

    def take_screenshots(self):
        """
        Runs through the process of taking all screenshots.
        """
        self.current_datetime_string = util.get_current_datetime_string()
        images = []
        for image in self.config.get('images'):
            self.get_target_config(image)
            self.add_filepaths(image)
            try:
                self.depict(
                    image.get('url'),
                    image.get('selector', 'body'),
                    image.get('local_filepath'),
                    # Depict's delay argument is defined in milliseconds
                    str(int(self.config.get('page_load_delay', 2)) * 1000)
                )
                images.append({
                    'slug': image.get('slug'),
                    'filepath': image.get('filepath'),
                    'local_filepath': image.get('local_filepath'),
                    'aws_filepath': image.get('aws_filepath'),
                    'aws_latest_filepath': image.get('aws_latest_filepath'),
                })
            except RuntimeError as e:
                logging.error(e)
        return images

    def add_filepaths(self, image):
        image['filepath'] = util.generate_image_filepath(
                self.current_datetime_string, image.get('slug'))
        image['local_filepath'] = util.generate_image_local_filepath(
                self.config.get('local_image_directory'),
                self.current_datetime_string, image.get('slug'))
        image['aws_filepath'] = util.generate_image_aws_filepath(
                self.config.get('aws_subpath'),
                self.current_datetime_string, image.get('slug'))
        image['aws_latest_filepath'] = util.generate_image_aws_latest_filepath(
                self.config.get('aws_subpath'), image.get('slug'))

    def depict(self, url, selector, destination, page_load_delay):
        """
        Runs the command-line utility `depict`.
        """
        args = ['depict', url, destination, '-s', selector,
                '--delay', page_load_delay]

        override_css_file = self.config.get('override_css_file')
        if override_css_file:
            args = args + ['--css', override_css_file]

        if self.config.get('wait_for_js_signal', False):
            args = args + ['--call-phantom']

        logging.info('Running shell command: %s' % (args))

        p = subprocess.Popen(args, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

        # Wait at most `failure_timeout` seconds for the process to finish
        failure_timeout = self.config.get('failure_timeout', 30)
        deadline = time.time() + failure_timeout
        while time.time() < deadline and p.poll() == None:
            time.sleep(1)

        # If the failure timeout is more than 0 and the process still hasn't
        # finished, terminate it.
        if failure_timeout > 0 and p.poll() == None:
            p.terminate()
            raise RuntimeError('Terminated shell command: %s' % (args))

        out, err = p.communicate()
        if p.returncode != 0:
            raise RuntimeError('depict error: %s' % err)
