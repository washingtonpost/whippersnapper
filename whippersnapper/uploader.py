import logging

from boto.s3.connection import Key, S3Connection

class Uploader(object):
    """
    Implements all upload-related logic.
    """

    def __init__(self, config):
        self.config = config
        conn = S3Connection(self.config.get('aws_access_key'),
                self.config.get('aws_secret_key'))

        # The bucket must already exist.
        self.bucket = conn.get_bucket(self.config.get('aws_bucket'))

    def upload_screenshots(self, images):
        """
        Runs through the process of uploading all screenshots.

        Uploads each image to both its filepath and the "latest" filepath.
        """
        filepaths = []
        for image in images:
            filepaths.append(self.upload(image.local_filepath,
                    image.aws_filepath))
            logging.info('Sucessfully uploaded image to %s' % image.public_url)

            filepaths.append(self.upload(image.local_filepath,
                    image.aws_latest_filepath))
            logging.info('Sucessfully uploaded image to %s'
                    % image.public_latest_url)
        return filepaths

    def upload(self, local_filepath, aws_filepath):
        """
        Uploads `local_filepath` to `aws_filepath`.

        Returns the published URL for the file.
        """
        logging.info('Publishing %s to %s' % (
                local_filepath, aws_filepath))

        key = Key(bucket=self.bucket, name=aws_filepath)
        key.key = aws_filepath
        key.set_contents_from_filename(local_filepath)
        key.set_acl('public-read')
