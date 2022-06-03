from pprint import pprint
from collections import Counter
from knn3_query import get_all_nftholder_for_each_contract, get_contract_address
import requests
import json
from requests.structures import CaseInsensitiveDict


def run_query(query):
    request = requests.post('https://mw.graphql.knn3.xyz/', json={'query': query}, timeout=1.5)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, query))


# get topk ranking collections
# user belong to which collection
# calculate the similarity between topk and specific collection
# recommend top holder name into recommend list


API_ID = 'HAe0ClnN'
API_SECRET = 'bd73ede59d49f0b9f59d66d154cef144cbeddfbc'
headers = CaseInsensitiveDict()
headers["X-API-KEY"] = API_ID


def get_user_most_like_contract(account_id):
    transaction_account_url = f'https://restapi.nftscan.com/api/v2/transactions/account/{account_id}?limit=50'
    resp = requests.get(transaction_account_url, headers=headers)
    data = json.loads(resp.text)['data']['content']
    if len(data) == 0:
        return None
    [(contract_name, _)] = Counter(item['contract_address'] for item in data).most_common(1)
    return contract_name


def get_account_belong_contract(contract_address, num):
    transaction_account_url = f'https://restapi.nftscan.com/api/v2/transactions/{contract_address}?limit={num}'
    resp = requests.get(transaction_account_url, headers=headers)
    data = json.loads(resp.text)['data']['content']
    # print(data)
    nft_holders = set()
    for item in data:
        nft_holders.add(item['from'])
    return list(nft_holders)


def get_assets(account_address):
    assests_account_url = f'https://restapi.nftscan.com/api/v2/account/own/all/{account_address}?erc_type= erc721&limit=10'
    resp = requests.get(assests_account_url, headers=headers)
    data = json.loads(resp.text)
    print(data)


def get_rec_lst(symbol_lst):
    contract_address_lst = []
    for symbol in symbol_lst:
        contract_address_lst.append(get_contract_address(symbol, 0))
    nft_holders = []
    for contract in contract_address_lst:
        nft_holders.extend(get_account_belong_contract(contract, 70))
    print(nft_holders)

    contract_lst = []
    i = 0
    for account in nft_holders:
        i += 1
        print(f'Deal with {i}st user')
        ret = get_user_most_like_contract(account)
        if not ret:
            continue
        contract_lst.append(ret)
    ret = Counter(contract_lst).most_common(5)
    print(ret)
    contract_set = set()
    for item in ret:
        contract_set.add(item[0])
    contract_lst = list(contract_set)
    rec_lst = []
    for contract in contract_lst:
        rec_lst.extend(get_account_belong_contract(contract, 100))
    return rec_lst


if __name__ == "__main__":
    n = int(float(input("Enter number of nft symbols : ")))
    print(n)
    symbol_lst = []
    for i in range(n):
        ele = input("Enter name of nft symbols (in a capital word) : ")
        symbol_lst.append(ele)  # adding the element
    print("symbol lst", symbol_lst)
    # symbol = input("Enter your value: ")
    # symbol = CRYPTOPUNKS
    rec_lst = get_rec_lst(symbol_lst)
    print("Here is our recommended user address: ", rec_lst)
    print("Length of rec list is: ", len(rec_lst))
