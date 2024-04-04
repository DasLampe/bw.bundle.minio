defaults = {
    'minio': {
        'version': '20240330094156.0.0',
        'checksum': 'ec5ba2c63b9815ea8e68a809240538b889fdbe22a8164dfe525c79b8986421b1',
        'path': '/usr/local/bin/minio',
        'user': 'minio',
        'group': 'minio',
        'address': '',
        'port': '9000',
        'console_port': '9001',
        'server_url': 'https://minio.example.org',
        #'console_url': 'https://minio.example.org/minio/ui',
        'accept_iptables': False,
        'data_path': '/media/cache',

        'root_user': 'root',
        'root_password': repo.vault.password_for(f'minio_root_user_{node.hostname}').value,
    },
}

@metadata_reactor
def compatibility_minio(metadata):
    return_value = {
        'minio': {},
    }

    # Rename access_key and secret_key to root_user and root_password
    if metadata.get('minio/access_key', '') and not metadata.get('minio/root_user'):
        return_value['minio']['root_user'] = metadata.get('minio/access_key')
    if metadata.get('minio/secret_key', '') and not metadata.get('minio/root_password'):
        return_value['minio']['root_password'] = metadata.get('minio/secret_key')

    return return_value

@metadata_reactor
def add_minio_user(metadata):
    if node.has_bundle('users'):
        return {
            'users': {
                metadata.get('minio').get('user'): {
                    'gid': metadata.get('minio').get('group'),
                }
            }
        }
    else:
        raise DoNotRunAgain

@metadata_reactor
def add_minio_iptables(metadata):
    if not node.has_bundle('iptables') or not metadata.get('minio/accept_iptables'):
        raise DoNotRunAgain

    interfaces = ['main_interface']

    iptables_rules = {}
    for interface in interfaces:
        iptables_rules += repo.libs.iptables.accept(). \
            input(interface). \
            tcp(). \
            dest_port(metadata.get('minio/port'))
        iptables_rules += repo.libs.iptables.accept(). \
            input(interface). \
            tcp(). \
            dest_port(metadata.get('minio/console_port'))

    return iptables_rules
