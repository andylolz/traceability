from itertools import zip_longest

import iatikit
import redis


r = redis.Redis()


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
