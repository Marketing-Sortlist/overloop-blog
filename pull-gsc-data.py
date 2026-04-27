#!/usr/bin/env python3
"""Pull GSC page data for overloop.com/blog/* and save to gsc-data.json"""
import json, warnings
warnings.filterwarnings('ignore')
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load SA from 1Password export
with open('seo-sa.json') as f:
    data = json.load(f)
fields = {f.get('label', f.get('id', '')): f.get('value', '') for f in data.get('fields', [])}
pk = fields.get('private_key', '').replace('\\\\n', '\\n')
if '\\n' in pk and chr(10) not in pk:
    pk = pk.encode().decode('unicode_escape')
sa = {k: fields.get(k, '') for k in ['type', 'project_id', 'private_key_id', 'client_email', 'client_id', 'auth_uri', 'token_uri', 'auth_provider_x509_cert_url', 'client_x509_cert_url', 'universe_domain']}
sa['private_key'] = pk

creds = service_account.Credentials.from_service_account_info(sa, scopes=['https://www.googleapis.com/auth/webmasters.readonly'])
service = build('searchconsole', 'v1', credentials=creds)

response = service.searchanalytics().query(
    siteUrl='sc-domain:overloop.com',
    body={
        'startDate': '2026-01-15',
        'endDate': '2026-04-14',
        'dimensions': ['page'],
        'dimensionFilterGroups': [{
            'filters': [{'dimension': 'page', 'operator': 'contains', 'expression': '/blog/'}]
        }],
        'rowLimit': 1000
    }
).execute()

rows = response.get('rows', [])
result = []
for r in rows:
    result.append({
        'page': r['keys'][0],
        'clicks': r.get('clicks', 0),
        'impressions': r.get('impressions', 0),
        'ctr': round(r.get('ctr', 0), 4),
        'position': round(r.get('position', 0), 1)
    })
result.sort(key=lambda x: x['impressions'], reverse=True)

with open('gsc-data.json', 'w') as f:
    json.dump(result, f, indent=2)

print("Saved {} pages to gsc-data.json".format(len(result)))
