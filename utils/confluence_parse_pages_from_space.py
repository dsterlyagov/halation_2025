from atlassian import Confluence

"получаем все id страниц с нужного пространства в данном случае"
confluence_url=''
username=''
password=''
confluence = Confluence(url=confluence_url, username=username, password=password, verify_ssl=False)
space = ''
res = confluence.get_all_pages_from_space(space, start=0, limit=100, status=None, expand=None, content_type='page')
print(res)
#print(len(res))
#print([r['id'] for r in res])
