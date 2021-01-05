defaults = {
    'minio': {
        'user': 'minio',
        'group': 'minio',
    }
}

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
    if not node.has_bundle('iptables'):
        raise DoNotRunAgain

    interfaces = ['main_interface']

    iptables_rules = {}
    for interface in interfaces:
        iptables_rules += repo.libs.iptables.accept(). \
            input(interface). \
            tcp(). \
            dest_port(9000)

    return iptables_rules
