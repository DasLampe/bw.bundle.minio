minio = node.metadata.get('minio', {})

actions = {}

default_path = '/usr/local/bin/minio'
default_url = 'https://dl.min.io/server/minio/release/linux-amd64/minio.{}'.format(
    minio.get('version', 'RELEASE.2021-01-05T05-22-38Z')
)
default_data_path = '/media/cache'

downloads = {
    minio.get('path', default_path): {
        'url': minio.get('download_url', default_url),
        'sha256': minio.get('checksum', 'c18280dad1703f3f0a9041d40b34399836c4d2f94b05cf30adc75898495bd80e'),
        'owner': minio.get('user'),
        'group': minio.get('group'),
        'mode': '0750',
        'tags': [
            'minio_install'
        ],
        'triggers': [
            'svc_systemd:minio.service:restart',
        ]
    }
}

files = {
    '/home/minio/environment': {
        'source': 'home/minio/environment',
        'content_type': 'jinja2',
        'context': {
            'data_path': minio.get('data_path', default_data_path),
            'access_key': minio.get('access_key', repo.vault.password_for(
                'minio_cache_accesskey_{}'.format(node.hostname))),
            'secret_key': minio.get('secret_key', repo.vault.password_for(
                'minio_cache_secretkey_{}'.format(node.hostname))),
        },
        'owner': minio.get('user'),
        'group': minio.get('group'),
        'tags': [
            'minio_install'
        ],
        'triggers': [
            'svc_systemd:minio.service:restart',
        ]
    },
    '/etc/systemd/system/minio.service': {
        'source': 'etc/systemd/system/minio.service',
        'content_type': 'jinja2',
        'context': {
            'user': minio.get('user'),
            'group': minio.get('group'),
            'path': minio.get('path', default_path),
            'environment_file': '/home/minio/environment',
        },
        'tags': [
            'minio_install'
        ],
        'triggers': [
            'svc_systemd:minio.service:restart',
        ]
    }
}

directories = {
    minio.get('data_path', default_data_path): {
        'owner': minio.get('user'),
        'group': minio.get('group'),
        'tags': [
            'minio_install'
        ]
    }
}

svc_systemd = {
    'minio.service': {
        'enabled': True,
        'running': True,
        'needs': [
            'tag:minio_install',
        ]
    }
}