
from urllib.parse import urlparse, parse_qsl
import os
from dataspin.providers.aws import S3StorageProvider
from dataspin.providers.local import LocalStorageProvider
from dataspin.providers.tencent import COSStorageProvider

from dataspin.utils.common import parse_scheme
    

def get_provider(url):
    parsed = urlparse(url)
    params = dict(host=parsed.netloc, name=os.path.basename(parsed.path))
    for key, value in parse_qsl(parsed.query):
        if key not in params:
            params[key] = value

    options, platform = parse_scheme(parsed.scheme)
    if platform in ["s3", "sqs"]:
        from .aws import SQSStreamProvider, S3StorageProvider
        if platform == 's3':
            path = parsed.path.strip('/')
            return S3StorageProvider(path,**params)
        if platform == 'sqs':
            return SQSStreamProvider(**params)
    elif platform in ["local", "file"]:
        path = os.path.join(parsed.netloc, parsed.path[1:])
        from .local import LocalStreamProvider, LocalStorageProvider
        if platform == "local":
            return LocalStreamProvider(path, options)
        if platform == 'file':
            return LocalStorageProvider(path, options)
    elif platform in ["cos","tdmq"]:
        from .tencent import COSStorageProvider,TDMQStreamProvider
        if platform == 'cos':
            path = parsed.path.strip('/')
            return COSStorageProvider(path,**params)
        if platform == 'tdmq':
            return TDMQStreamProvider(**params)
    raise Exception(f'No provider for platform {platform}')

