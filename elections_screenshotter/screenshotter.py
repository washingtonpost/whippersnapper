import datetime
import logging
import subprocess
import time

import util

class Screenshotter(object):
    """
    Implements all screenshot-related logic.
    """

    def __init__(self, config):
        self.config = config
        self.screenshot_filenames = []

    def take_screenshots(self):
        """
        Runs through the process of taking all screenshots.
        """
        self.current_datetime_string = util.get_current_datetime_string()
        images = []
        for image in self.config.get('images'):
            self.add_filepaths(image)
            try:
                self.depict(
                    image.get('url'),
                    image.get('selector'),
                    image.get('local_filepath'),
                    str(self.config.get('depict_timeout'))
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
                self.config.get('local_root'),
                self.current_datetime_string, image.get('slug'))
        image['aws_filepath'] = util.generate_image_aws_filepath(
                self.config.get('aws_root'),
                self.current_datetime_string, image.get('slug'))
        image['aws_latest_filepath'] = util.generate_image_aws_latest_filepath(
                self.config.get('aws_root'), image.get('slug'))

    def depict(self, url, selector, destination, timeout):
        """
        Runs the command-line utility `depict`.
        """
        args = ['depict', url, destination, '-s', selector]

        depict_css_file = self.config.get('depict_css_file')
        if depict_css_file:
            args = args + ['--css', depict_css_file]

        if self.config.get('depict_wait_for_js'):
            args = args + ['--call-phantom', '--call-phantom-timeout', timeout]

        logging.info('Running shell command: %s' % (args))

        p = subprocess.Popen(args, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

        deadline = time.time() + self.config.get('screenshot_timeout')
        while time.time() < deadline and p.poll() == None:
            time.sleep(1)

        if p.poll() == None:
            p.terminate()
            raise RuntimeError('Terminated shell command: %s' % (args))

        out, err = p.communicate()
        if p.returncode != 0:
            raise RuntimeError('depict error: %s' % err)
