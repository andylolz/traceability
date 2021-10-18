import csv
from collections import defaultdict
from itertools import zip_longest
from os.path import join

import iatikit
import redis


r = redis.Redis()
iatikit.download.data()


for pub in iatikit.data().publishers:
    for act in pub.activities:
        if act.id is not None:
            _ = r.set(act.id, pub.name)


store = []
for pub in iatikit.data().publishers:
    for act in pub.activities:
        receiver_ids = act.etree.xpath(
            'transaction/receiver-org/@receiver-activity-id')
        provider_ids = act.etree.xpath(
            'transaction/provider-org/@provider-activity-id')
        links = []
        for provider_id, receiver_id in zip_longest(provider_ids, receiver_ids,
                                                    fillvalue=act.id):
            if not receiver_id:
                continue
            if not provider_id:
                continue
            receiver = r.get(receiver_id)
            if receiver:
                receiver = receiver.decode()
            else:
                continue
            provider = r.get(provider_id)
            if provider:
                provider = provider.decode()
            else:
                continue
            if provider == pub.name:
                direction = 'downstream'
            if receiver == pub.name:
                direction = 'upstream'
            if receiver != pub.name or provider != pub.name:
                tup = (direction, provider, receiver)
                links.append(tup)
        links = list(set(links))
        for link in links:
            print(link)
            store.append(link)

dedupe_store = defaultdict(int)
for link in store:
    dedupe_store[link] += 1

dedupe_store = sorted([{
        'type': k[0],
        'source': k[1],
        'target': k[2],
        'weight': v,
    } for k, v in dedupe_store.items()],
    key=lambda x: list(x.values()))

fieldnames = ['source', 'target', 'type', 'weight']
with open(join('output', 'links.csv'), 'w') as handler:
    writer = csv.DictWriter(handler, fieldnames=fieldnames)
    writer.writeheader()
    _ = [writer.writerow(x) for x in dedupe_store]
