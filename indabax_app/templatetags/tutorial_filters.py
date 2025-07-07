from django import template
from urllib.parse import urlparse, parse_qs

register = template.Library()

@register.filter
def youtube_video_id(value):
    """
    Extracts the YouTube video ID from a given URL.
    Handles watch?v=, https://www.youtube.com/watch?v=VIDEO_ID, and embed/ URLs.
    """
    if not value:
        return None

    parsed_url = urlparse(value)

    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            query = parse_qs(parsed_url.query)
            return query.get('v', [None])[0]
        elif parsed_url.path.startswith('/embed/'):
            return parsed_url.path.split('/')[2]
    elif parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:] # Remove leading '/'
    return None