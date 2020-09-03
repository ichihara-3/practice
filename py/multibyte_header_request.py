import urllib.request

def main():
    req = urllib.request.Request('http://localhost:8080', headers={'User-Agent': 'ほげ'.encode('utf-8').decode('latin-1')}, method='GET')
    with urllib.request.urlopen(req) as f:
        print(f.read().decode('utf-8'))


if __name__ == '__main__':
    main()
