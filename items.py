cfg = node.metadata.get('minio', {})

downloads = {
    f'/tmp/minio_{cfg.get("version")}.deb': {
        'url':  f'https://dl.min.io/server/minio/release/linux-amd64/minio_{cfg.get("version")}_amd64.deb',
        'sha256': cfg.get('checksum'),
        'owner': cfg.get('user'),
        'group': cfg.get('group'),
        'tags': [
            'minio_install'
        ],
    }
}

actions = {
    'install_minio': {
        'command': f'dpkg -i /tmp/minio_{cfg.get("version")}.deb',
        'needs': [
            f'download:/tmp/minio_{cfg.get("version")}.deb',
        ],
        'tags': [
            'minio_install',
        ],
        'triggers': [
            'svc_systemd:minio.service:restart',
        ],
    },
    'daemon_reload': {
        'command': 'systemctl daemon-reload',
        'triggered': True,
        'triggers': [
            'svc_systemd:minio.service:restart',
        ],
    }
}

files = {
    '/etc/systemd/system/minio.service': {
        'source': 'etc/systemd/system/minio.service.j2',
        'content_type': 'jinja2',
        'context': {
            'cfg': cfg,
        },
        'tags': [
            'minio_install'
        ],
        'triggers': [
            'svc_systemd:minio.service:restart',
            'action:daemon_reload',
        ],
    }
}

directories = {
    cfg.get('data_path'): {
        'owner': cfg.get('user'),
        'group': cfg.get('group'),
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
