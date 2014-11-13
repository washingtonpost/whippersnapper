import datetime

def generate_image_filepath(current_datetime_string, slug):
    """
    Generates a filepath for the image in the following form:

    slug/YYYY-MM-DD-HHMMSS-slug.png

    Used to generate local and aws filepaths.
    """
    return '%s/%s-%s.png' % (slug, current_datetime_string, slug)

def generate_image_local_filepath(local_image_directory,
        current_datetime_string, slug):
    """
    Generates a local filepath for the image, using
    `generate_image_filepath()`
    """
    return '%s/%s' % (local_image_directory,
            generate_image_filepath(current_datetime_string, slug))

def generate_image_aws_filepath(aws_root, current_datetime_string, slug):
    """
    Generates an aws filepath for the image, using
    `generate_image_filepath()`
    """
    return '%s/%s' % (aws_root,
            generate_image_filepath(current_datetime_string, slug))

def generate_image_aws_latest_filepath(aws_root, slug):
    """
    Generates an aws "latest" filepath for the image.
    """
    return '%s/%s/latest-%s.png' % (aws_root, slug, slug)

def generate_public_url(aws_bucket, aws_filepath):
        """
        Generates a public URL for the file.
        """
        return 'http://s3.amazonaws.com/%s/%s' % (aws_bucket, aws_filepath)

def get_current_datetime_string():
    """
    Returns the current time in a string suitable for filenames.
    """
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d-%H%M%S')
