import json
import time
from urllib import request, error

BASE = 'http://127.0.0.1:8000/api/empresas/'
TOKEN = '35c3a8a22d02f5b971c57182af8469504612416f'
HEADERS = {
    'Authorization': f'Token {TOKEN}',
    'Content-Type': 'application/json',
}

def req(url, method='GET', data=None):
    data_bytes = None
    if data is not None:
        data_bytes = json.dumps(data).encode('utf-8')
    req = request.Request(url, data=data_bytes, method=method)
    for k, v in HEADERS.items():
        req.add_header(k, v)
    try:
        with request.urlopen(req, timeout=5) as resp:
            body = resp.read().decode('utf-8')
            print(f"{method} {url} -> {resp.status}")
            if body:
                try:
                    print(json.dumps(json.loads(body), indent=2, ensure_ascii=False))
                except Exception:
                    print(body)
            return resp.status, body
    except error.HTTPError as e:
        body = e.read().decode('utf-8') if e.fp else ''
        print(f"{method} {url} -> {e.code}")
        print(body)
        return e.code, body
    except Exception as e:
        print('Error:', e)
        return None, None


if __name__ == '__main__':
    print('Waiting 1s for server...')
    time.sleep(1)

    # 1. GET list
    req(BASE)

    # 2. POST create
    new = {
        "ruc": "80012345-6",
        "nombre": "ACME S.A.",
        "sector": "Tecnología",
        "email": "contacto@acme.com",
        "telefono": "+595 21 123456",
        "direccion": "Av. Principal 123, Asunción"
    }
    status, body = req(BASE, method='POST', data=new)
    created = None
    if status in (200,201) and body:
        try:
            created = json.loads(body)
        except Exception:
            pass

    # 3. GET detail
    if created:
        pk = created.get('id')
        req(f"{BASE}{pk}/")

        # 4. PATCH
        patch = {"email": "nuevo@acme.com", "telefono": "+595 21 999888"}
        req(f"{BASE}{pk}/", method='PATCH', data=patch)

        # 5. DELETE
        req(f"{BASE}{pk}/", method='DELETE')
