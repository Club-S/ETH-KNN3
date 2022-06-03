import requests
from pprint import pprint


def run_query(query):
    request = requests.post('https://mw.graphql.knn3.xyz/', json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, query))

s = """
    query {{
  nfts(where:{{symbol: "{0}"}}) {{
    contract
    symbol
    addrsHold (options:{{limit:10, offset:{1}}}){{
      address
    }}
  }}
}}"""


def get_contract_address(symbol, offset):
    query = s.format(symbol, offset)
    # print(query)
    data = run_query(query)
    return data['data']['nfts'][0]['contract']


def get_all_nftholder_for_each_contract(symbol, offset):
    query = s.format(symbol, offset)
    # print(query)
    data = run_query(query)
    # print the results
    if len(data['data']['nfts']) == 0:
        return []
    nft_lst = data['data']['nfts'][0]['addrsHold']
    nfts = []
    for item in nft_lst:
        nfts.append(item['address'])
    return nfts


if __name__ == "__main__":
    symbol = "CRYPTOPUNKS"
    # contract_address = "0x81ae0be3a8044772d04f32398bac1e1b4b215aa8"
    offset = 0
    # get_all_nftholder_for_each_contract()
    nfts = get_all_nftholder_for_each_contract(symbol, offset)
    pprint(nfts)