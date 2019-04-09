import requests
from requests_toolbelt import MultipartEncoder
from urllib.parse import urljoin


class Asset():
    def __init__(self, name, content, content_type, content_size):
        self.name = name
        self.content = content
        self.content_type = content_type
        self.content_size = content_size

    def upload(self, container):
        resp = container.send_action(
            'asset:put',
            {
                'filename': self.name,
                'content-type': self.content_type,
                'content-size': self.content_size,
            }
        )

        if ('result' in resp) and ('post-request' in resp['result']):
            post_request = resp['result']['post-request']

            post_url = self._build_post_url(post_request, container)
            multipart_encoder = self._build_multipart_encoder(
                post_request, container)

            headers = {
                'Content-Type': multipart_encoder.content_type,
                'X-Skygear-API-Key': container.api_key
            }

            post_resp = requests.post(
                post_url,
                headers=headers,
                data=multipart_encoder)

            if post_resp.ok:
                return resp['result']['asset']['$name']

        return None

    def _build_post_url(self, post_request, container):
        post_url = post_request['action']

        if post_url[0] == '/':
            post_url = post_url[1:]

        if not post_url.startswith('http'):
            post_url = urljoin(container.endpoint, post_url)

        return post_url

    def _build_multipart_encoder(self, post_request, container):
        fields = []

        if 'extra-fields' in post_request:
            for key, value in post_request['extra-fields'].items():
                fields.append((key, value))

        fields.append(('file', ('blob', self.content, self.content_type)))

        return MultipartEncoder(fields)


def build_image_asset_from_url(url, filename):
    content = requests.get(url).content
    return Asset(
        filename,
        content,
        'image/jpeg',
        len(content),
    )
