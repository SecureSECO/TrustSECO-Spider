import subprocess

print('Starting scan...')

link = 'https://github.com/LiveTL/HyperChat/releases/download/v2.5.5/HyperChat-Chrome.zip'

args = ['wget', '-qO-', link, '|', 'clamdscan',
        '--config-file=clamav/configs/client_config.conf', '-']

result = subprocess.run(args, capture_output=True, encoding='utf-8')

print('Scan complete.')

print('Result:')
print(result.stdout)
