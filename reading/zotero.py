from pyzotero import zotero

def fetch_list(library_id, library_type, collection_key, api_key, csl):
    zot = zotero.Zotero(library_id, library_type, api_key)
    collections = zot.collections_top()
    data = {}
    if collection_key:
        data = {'ref_list': zot.collection_items_top(
            collection_key,
            content = 'bib', 
            style = csl, 
            sort = 'creator',
            direction = 'asc',
            linkwrap=1
            ), 'metadata':  zot.collection_items_top(
            collection_key,
            sort = 'creator',
            direction = 'asc'
            )
        }
    else:
        for c in collections:
            name = c['data']['name']
            subs = zot.collections_sub(c['key'])
            if len(subs) > 1:
                data[name] = {}
                for s in subs:
                    sub_name = s['data']['name']
                    s_key = s['key']
                    print(name, sub_name, s_key)
                    data[name][sub_name] = {
                        'contents': zot.collection_items_top(
                            s_key, 
                            content = 'bib', 
                            style = csl, 
                            sort = 'creator',
                            direction = 'asc',
                            linkwrap=1
                            )
                        }
            else:
                key = c['key']
                data[name] = {
                    'contents': zot.collection_items_top(
                        key, 
                        content = 'bib', 
                        style = csl, 
                        sort = 'creator',
                        direction = 'asc',
                        linkwrap=1
                        )
                    }
    return(data)