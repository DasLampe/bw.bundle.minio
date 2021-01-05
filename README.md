# MinIO - Bundlewrap
Install and configure MinIO via [Bundlewrap](https://bundlewrap.org).

## Config
```python
node['my-node'] = {
    'metadata': {
        'minio': {
            'version': 'RELEASE.2021-01-05T05-22-38Z',
            'checksum': 'c18280dad1703f3f0a9041d40b34399836c4d2f94b05cf30adc75898495bd80e',
            'download_url': 'https://dl.min.io/server/minio/release/linux-amd64/minio.RELEASE.2021-01-05T05-22-38Z',
            'path': '/usr/local/bin/minio',
            'user': 'minio',
            'group': 'minio',
            'data_path': '/media/cache',
            'access_key': vault.password_for('minio_cache_accesskey_NodeHostName'),
            'secret_key': vault.password_for('minio_cache_secretkey_NodeHostName'),
        }
    }
}

```

## Dependecies
- [Item Download](https://github.com/sHorst/bw.item.download)

## Supports
- (Ubuntu) Linux