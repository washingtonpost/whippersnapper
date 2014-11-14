import datetime
import logging
import pipes
import subprocess
import time

import target

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
        targets = []
        for target_config in self.config.get('targets'):
            current_target = target.Target(self.config, target_config)
            try:
                self.depict(
                    current_target.url,
                    current_target.selector,
                    current_target.local_filepath,
                    # Depict's delay argument is defined in milliseconds
                    str(int(current_target.page_load_delay) * 1000)
                )
                targets.append(current_target)
            except RuntimeError as e:
                logging.error(e)
        return targets

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

        # Quote each argument and combine them into a single string
        args_string = ''
        for arg in args:
            quoted_arg = pipes.quote(arg)
            args_string += ' ' + quoted_arg

        logging.info('Running shell command: %s' % (args_string))

        # Use shell=True because selectors may contain characters that would
        # otherwise be stripped out by subprocess.Popen() (e.g. `#`, `<`, etc.
        p = subprocess.Popen(args_string, shell=True, stdout=subprocess.PIPE,
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
