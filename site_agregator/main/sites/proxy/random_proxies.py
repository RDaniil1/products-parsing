import random
from pathlib import Path


def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile, 2):
        if random.randrange(num):
            continue
        line = aline
    return line

def get_random_proxy(proxy_type: str='socks5'):
    if proxy_type not in ['socks5', 'socks4', 'http']:
        return
    
    proxy = ''
    with open(Path(__file__).parent / f'{proxy_type}.txt') as file:
        proxy = random_line(file)

    return proxy.replace('\n', '')

if __name__ == '__main__':
    print(get_random_proxy())