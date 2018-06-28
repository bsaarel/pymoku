import pkg_resources as pkr

# List of compatible firmware builds
compat_fw = [474]

# List of compatible patches
compat_patch = [1]

# List of compatible packs
compat_packs = [('python-pymoku',	'CBA6E57F52D0A312C46CF66A70BA8DFB1E237AD9'),
				('mercury',			'CBA6E57F52D0A312C46CF66A70BA8DFB1E237AD9')]

# Compatible network protocol version
protocol_version = '7'

# Official release name
release = pkr.resource_stream(__name__, "version.txt").read().decode('utf-8')
