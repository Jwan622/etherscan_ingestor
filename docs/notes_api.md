# Notes on the etherscan api

Here are some observations on the internal transactions API:
https://docs.etherscan.io/api-endpoints/accounts#get-a-list-of-internal-transactions-by-address

## Block Numbers

- block numbers can be the same. So multiple transactions on a block Example:

```json
{"block_number":"12376282","time_stamp":"1620244704","hash":"0x1a8fc72f3ee2298234b862908eb710d0f83403fade6c2840e2d03e233d40de46","from":"0xe592427a0aece92de3edee1f18e0157c05861564","to":"0x38fffdcab90891d776342272b6e33b8cafecac3d","value":"205806336784777948","contractAddress":"","input":"","type":"call","gas":"14218","gas_used":"0","traceId":"1_2","isError":"0","errCode":""},{"block_number":"12376285","time_stamp":"1620244740","hash":"0x3689ce29d0147b652a68d2e1ca43a753ad80fcbbfe9844433af6d559e75fe429","from":"0xe592427a0aece92de3edee1f18e0157c05861564","to":"0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2","value":"29000000000000000","contractAddress":"","input":"","type":"call","gas":"51244","gas_used":"23974","traceId":"0_2_0","isError":"0","errCode":""},
```

What's the implication of this you ask? You can't just simply give the API a range of 10k for the block numbers and expected 10k transactions. Well... you will since it limits you to 10k, But that means there's more transasctions in that 10k block window. So you need to dynmically adjust the API call until you get fewer than 10k transactions. Lol, this is the trick to all of this!
- `sort` affects the timestamp and block_number returned. `sort=desc` will return the most recent transaction for an account and `sort=asc` will return the earliest.
- hashes are unique according to the docs
- the 10k limit is annoying, need to find a way to make sure we're not missing data. play around with offset and page combinations.
- page and offset can be changed but the multiplication of the two cannot be over 10000. I think we just leave page=1 and offset=10000 and play around with the block number range.
- The startblock and endblock affect the block_number returned. If an account has more than 10000 transactions, this is how to change the window of blocks to retrieve. 



start and end block are inclusive. This api call:

```bash
https://api.etherscan.io/api?module=account&action=txlistinternal&address=0xE592427A0AEce92De3Edee1F18E0157C05861564&startblock=12380435&endblock=12380436&page=1&offset=10000&sort=asc&apikey=H4PV22WR9MSNYJM25TN9FFXEZGB3NFDX6V
```

returns this:

```bash
{"status":"1","message":"OK","result":[{"block_number":"12380435","time_stamp":"1620300159","hash":"0xb83988618e80851f33c8bec869c82ce73d5c2217a6def66ed2b796c06479779a","from":"0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2","to":"0xe592427a0aece92de3edee1f18e0157c05861564","value":"46396376127586676","contractAddress":"","input":"","type":"call","gas":"2300","gas_used":"83","traceId":"1_1_0","isError":"0","errCode":""},{"block_number":"12380435","time_stamp":"1620300159","hash":"0xb83988618e80851f33c8bec869c82ce73d5c2217a6def66ed2b796c06479779a","from":"0xe592427a0aece92de3edee1f18e0157c05861564","to":"0x2ee02d4e818e0e1ccc46054b2f7c8d10018cffc8","value":"46396376127586676","contractAddress":"","input":"","type":"call","gas":"18490","gas_used":"0","traceId":"1_2","isError":"0","errCode":""},{"block_number":"12380435","time_stamp":"1620300159","hash":"0x35eb84813adcedc87f773da468829c607dbca18cc41d5f7c585b93cdf4603892","from":"0xe592427a0aece92de3edee1f18e0157c05861564","to":"0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2","value":"447325850000000000","contractAddress":"","input":"","type":"call","gas":"50681","gas_used":"23974","traceId":"0_2_0","isError":"0","errCode":""},{"block_number":"12380435","time_stamp":"1620300159","hash":"0xfe2c454e2bc53507d049b370cba9cbcf380af946ee64bf88e803d1efe0174719","from":"0xe592427a0aece92de3edee1f18e0157c05861564","to":"0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2","value":"1200000000000000000","contractAddress":"","input":"","type":"call","gas":"82334","gas_used":"23974","traceId":"0_2_0","isError":"1","errCode":""},{"block_number":"12380435","time_stamp":"1620300159","hash":"0xf80e2d9f7b8d80dceb25253c686dde619f0999547510267a27d9524ee79e94ba","from":"0xe592427a0aece92de3edee1f18e0157c05861564","to":"0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2","value":"89071007452125217","contractAddress":"","input":"","type":"call","gas":"63207","gas_used":"23974","traceId":"0_0_2_0_2_0","isError":"0","errCode":""},{"block_number":"12380435","time_stamp":"1620300159","hash":"0xf80e2d9f7b8d80dceb25253c686dde619f0999547510267a27d9524ee79e94ba","from":"0xe592427a0aece92de3edee1f18e0157c05861564","to":"0xc514efd06ddd9c4c03a47a5aabee80d1c6372890","value":"383717952420338","contractAddress":"","input":"","type":"call","gas":"26637","gas_used":"0","traceId":"1_0","isError":"0","errCode":""},{"block_number":"12380435","time_stamp":"1620300159","hash":"0x179188799299b08302ff597f51a1923408358d35368ef92a566a90cf4f9eabf0","from":"0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2","to":"0xe592427a0aece92de3edee1f18e0157c05861564","value":"35924547841231012","contractAddress":"","input":"","type":"call","gas":"2300","gas_used":"83","traceId":"1_1_0","isError":"0","errCode":""},{"block_number":"12380435","time_stamp":"1620300159","hash":"0x179188799299b08302ff597f51a1923408358d35368ef92a566a90cf4f9eabf0","from":"0xe592427a0aece92de3edee1f18e0157c05861564","to":"0xc889b5cec86b56c724ba962877d1ea71f353428b","value":"35924547841231012","contractAddress":"","input":"","type":"call","gas":"17895","gas_used":"0","traceId":"1_2","isError":"0","errCode":""},{"block_number":"12380435","time_stamp":"1620300159","hash":"0xd0f8409372282ee21c711e4a467ed96fae74d9ea6193344de5a5ec70e7319c60","from":"0xe592427a0aece92de3edee1f18e0157c05861564","to":"0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2","value":"100000000000000000","contractAddress":"","input":"","type":"call","gas":"232036","gas_used":"23974","traceId":"0_2_0","isError":"1","errCode":""},{"block_number":"12380435","time_stamp":"1620300159","hash":"0x38fe60f33a4fcce5c68f45c4238d00544efab4582e5fa3db0dbbe968632ba288","from":"0xe592427a0aece92de3edee1f18e0157c05861564","to":"0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2","value":"20810660000000000","contractAddress":"","input":"","type":"call","gas":"50712","gas_used":"23974","traceId":"0_2_0","isError":"0","errCode":""},{"block_number":"12380435","time_stamp":"1620300159","hash":"0x0d683be49bae5cf06b1cc7399bf8d154eaf6264dffb9180649fa565a18673b23","from":"0xe592427a0aece92de3edee1f18e0157c05861564","to":"0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2","value":"62394530000000000","contractAddress":"","input":"","type":"call","gas":"51756","gas_used":"23974","traceId":"0_2_0","isError":"0","errCode":""},{"block_number":"12380436","time_stamp":"1620300162","hash":"0x3460148d88a910c069c46d55f4e45c469ac02b477a18f5f3bcf54109656410e3","from":"0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2","to":"0xe592427a0aece92de3edee1f18e0157c05861564","value":"344086525989323007","contractAddress":"","input":"","type":"call","gas":"2300","gas_used":"83","traceId":"1_1_0","isError":"0","errCode":""},{"block_number":"12380436","time_stamp":"1620300162","hash":"0x3460148d88a910c069c46d55f4e45c469ac02b477a18f5f3bcf54109656410e3","from":"0xe592427a0aece92de3edee1f18e0157c05861564","to":"0x5e458d943293a5f47a3a5438e40a23cd65790905","value":"344086525989323007","contractAddress":"","input":"","type":"call","gas":"25361","gas_used":"0","traceId":"1_2","isError":"0","errCode":""},{"block_number":"12380436","time_stamp":"1620300162","hash":"0x4b31dab3e1e4f0dba3dd60c3d1fd8602b03eb71093ceae7f2511daa8f8ce691a","from":"0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2","to":"0xe592427a0aece92de3edee1f18e0157c05861564","value":"810062896348093915","contractAddress":"","input":"","type":"call","gas":"2300","gas_used":"83","traceId":"1_1_0","isError":"0","errCode":""},{"block_number":"12380436","time_stamp":"1620300162","hash":"0x4b31dab3e1e4f0dba3dd60c3d1fd8602b03eb71093ceae7f2511daa8f8ce691a","from":"0xe592427a0aece92de3edee1f18e0157c05861564","to":"0x941f0ad4b130b157212b290b8931b91331c60911","value":"810062896348093915","contractAddress":"","input":"","type":"call","gas":"18356","gas_used":"0","traceId":"1_2","isError":"0","errCode":""}]}
```

So a diff in 1 block in the api call can return multiple transactions but 2 blocks.

## Are hashes unique?
Also I don't think hashes are unique on etherscan? At least not in the API? 

```bash
[SQL: INSERT INTO transactions ("block_number", "time_stamp", hash, from_address_id, to_address_id, value, gas, "gas_used", "isError") VALUES (%(block_number)s, %(time_stamp)s, %(hash)s, %(from_address_id)s,
%(to_address_id)s, %(value)s, %(gas)s, %(gas_used)s, %(isError)s)]
[parameters: ({'block_number': 12371051, 'time_stamp': 1620175296, 'hash': '0x5cdf9ec984fb0fe801cc529c003bcdd5271857103c19cd25b887deb8eaaecaff', 'from_address_id': 1, 'to_address_id': 2, 'value':
100000000000000000, 'gas': 48969, 'gas_used': 23974, 'isError': 0}, {'block_number': 12371376, 'time_stamp': 1620179783, 'hash': '0xce7c3c307d820785caa12938012372fc9366a614a6aacf8ba9ddb2b6497b7ff5',
'from_address_id': 1, 'to_address_id': 2, 'value': 100000000000000, 'gas': 53026, 'gas_used': 23974, 'isError': 0}, {'block_number': 12371525, 'time_stamp': 1620181866, 'hash':
'0xc9c50c8d403dfe2545e467a2015d7b6311a9c26d3ab84c1985ec76de71efbfb7', 'from_address_id': 2, 'to_address_id': 1, 'value': 98196148135983, 'gas': 2300, 'gas_used': 83, 'isError': 0}, {'block_number': 12371525,
'time_stamp': 1620181866, 'hash': '0xc9c50c8d403dfe2545e467a2015d7b6311a9c26d3ab84c1985ec76de71efbfb7', 'from_address_id': 1, 'to_address_id': 4, 'value': 98196148135983, 'gas': 23999, 'gas_used': 0, 'isError':
0})]
```

I found it here:

https://etherscan.io/tx/0xc9c50c8d403dfe2545e467a2015d7b6311a9c26d3ab84c1985ec76de71efbfb7#internal

It looks like this had 2 internal transactions (2 transactions) with the same hash. So perhaps remove the unique contraint on my table for now. Also when presenting the data, perhaps show that a transaction hash can be to and from a few different addresses (one hash, two internal transactions)


## Strategy to get all transctions for an account? 

**Problem**: How to get all transactions for a single account. What's our strat given the 10k limit?

**Thoughts** So here's what I think I'll do since there's a 10k limit and there are a lot of transactions per account.

For this address, we see this in the API if we play with the `sort=asc` and `sort=desc`:

```
first block_number: 12360000
last block_number: 19791167
```

On page 10, `sort=desc`, 1000 offset, last record = 19719682 so this is the 1000th to last record. Note this is more than 10k less than the last block_number

Also, on page 10, `sort=asc`, 1000 offset, last record = 12380435
so this is the 1000th from first record. It's more than 20k more than the first record.

Total block_number diff ~ 7 million blocks.
  
We can multithread the difference. Say we have 8 threads, we see this in our output:


```bash
2024-05-04 13:38:17,229 - INFO - Thread 0 processing from STARTING block 12369879 to ENDING block 13298427
2024-05-04 13:38:17,229 - INFO - Making an API call to Etherscan. current starting block: 12369879
2024-05-04 13:38:17,229 - INFO - Thread 1 processing from STARTING block 13298428 to ENDING block 14226976
2024-05-04 13:38:17,229 - INFO - Making an API call to Etherscan. current starting block: 13298428
2024-05-04 13:38:17,230 - INFO - Thread 2 processing from STARTING block 14226977 to ENDING block 15155525
2024-05-04 13:38:17,230 - INFO - Making an API call to Etherscan. current starting block: 14226977
2024-05-04 13:38:17,230 - INFO - Thread 3 processing from STARTING block 15155526 to ENDING block 16084074
2024-05-04 13:38:17,230 - INFO - Making an API call to Etherscan. current starting block: 15155526
2024-05-04 13:38:17,231 - INFO - Thread 4 processing from STARTING block 16084075 to ENDING block 17012623
2024-05-04 13:38:17,231 - INFO - Making an API call to Etherscan. current starting block: 16084075
2024-05-04 13:38:17,231 - INFO - Thread 5 processing from STARTING block 17012624 to ENDING block 17941172
2024-05-04 13:38:17,231 - INFO - Making an API call to Etherscan. current starting block: 17012624
2024-05-04 13:38:17,231 - INFO - Thread 6 processing from STARTING block 17941173 to ENDING block 18869721
2024-05-04 13:38:17,231 - INFO - Making an API call to Etherscan. current starting block: 17941173
2024-05-04 13:38:17,232 - INFO - Thread 7 processing from STARTING block 18869722 to ENDING block 19798275
2024-05-04 13:38:17,232 - INFO - Making an API call to Etherscan. current starting block: 18869722
...
2024-05-04 13:38:17,490 - DEBUG - https://api.etherscan.io:443 "GET /api?module=account&action=txlistinternal&address=0xE592427A0AEce92De3Edee1F18E0157C05861564&startblock=14226977&endblock=15155525&page=1&offset=10000&sort=asc&apikey=H4PV22WR9MSNYJM25TN9FFXEZGB3NFDX6V HTTP/1.1" 200 178
2024-05-04 13:38:17,510 - DEBUG - https://api.etherscan.io:443 "GET /api?module=account&action=txlistinternal&address=0xE592427A0AEce92De3Edee1F18E0157C05861564&startblock=16084075&endblock=17012623&page=1&offset=10000&sort=asc&apikey=H4PV22WR9MSNYJM25TN9FFXEZGB3NFDX6V HTTP/1.1" 200 178
2024-05-04 13:38:18,034 - DEBUG - https://api.etherscan.io:443 "GET /api?module=account&action=txlistinternal&address=0xE592427A0AEce92De3Edee1F18E0157C05861564&startblock=12369879&endblock=13298427&page=1&offset=10000&sort=asc&apikey=H4PV22WR9MSNYJM25TN9FFXEZGB3NFDX6V HTTP/1.1" 200 None
2024-05-04 13:38:18,170 - DEBUG - https://api.etherscan.io:443 "GET /api?module=account&action=txlistinternal&address=0xE592427A0AEce92De3Edee1F18E0157C05861564&startblock=17941173&endblock=18869721&page=1&offset=10000&sort=asc&apikey=H4PV22WR9MSNYJM25TN9FFXEZGB3NFDX6V HTTP/1.1" 200 None
2024-05-04 13:38:18,339 - DEBUG - https://api.etherscan.io:443 "GET /api?module=account&action=txlistinternal&address=0xE592427A0AEce92De3Edee1F18E0157C05861564&startblock=17012624&endblock=17941172&page=1&offset=10000&sort=asc&apikey=H4PV22WR9MSNYJM25TN9FFXEZGB3NFDX6V HTTP/1.1" 200 None
^C2024-05-04 13:38:18,956 - DEBUG - https://api.etherscan.io:443 "GET /api?module=account&action=txlistinternal&address=0xE592427A0AEce92De3Edee1F18E0157C05861564&startblock=13298428&endblock=14226976&page=1&offset=10000&sort=asc&apikey=H4PV22WR9MSNYJM25TN9FFXEZGB3NFDX6V HTTP/1.1" 200 None
2024-05-04 13:38:18,985 - DEBUG - https://api.etherscan.io:443 "GET /api?module=account&action=txlistinternal&address=0xE592427A0AEce92De3Edee1F18E0157C05861564&startblock=15155526&endblock=16084074&page=1&offset=10000&sort=asc&apikey=H4PV22WR9MSNYJM25TN9FFXEZGB3NFDX6V HTTP/1.1" 200 None
2024-05-04 13:38:19,027 - DEBUG - https://api.etherscan.io:443 "GET /api?module=account&action=txlistinternal&address=0xE592427A0AEce92De3Edee1F18E0157C05861564&startblock=18869722&endblock=19798275&page=1&offset=10000&sort=asc&apikey=H4PV22WR9MSNYJM25TN9FFXEZGB3NFDX6V HTTP/1.1" 200 None
```

the problem, we still have more than a 10k block diff for each thread:


```bash
2024-05-04 13:38:17,490 - DEBUG - https://api.etherscan.io:443 "GET /api?module=account&action=txlistinternal&address=0xE592427A0AEce92De3Edee1F18E0157C05861564&startblock=14226977&endblock=15155525&page=1&offset=10000&sort=asc&apikey=H4PV22WR9MSNYJM25TN9FFXEZGB3NFDX6V HTTP/1.1" 200 178
```

That's approx a 1 million diff between the start and end block. So within each thread, we need to divide and conquer too. So within our `ingest` method which is passed to each thread, we need to divide and conquer so that we get make calls in 10k chunks (or at least try to?) until we get to our end block. I think that's the strategy. 

## Length to ingest?

Using 16 threads, and dividing up teh 7 million blocks you have to traverse... about 2 hours. thread 2 actually takes teh longest (ending at block 13749431)

```python3
2024-05-05 21:41:26,948 - DEBUG - https://api.etherscan.io:443 "GET /api?module=account&action=txlistinternal&address=0xE592427A0AEce92De3Edee1F18E0157C05861564&startblock=13742944&endblock=13749431&page=1&offset=10000&sort=asc&apikey=H4PV22WR9MSNYJM25TN9FFXEZGB3NFDX6V HTTP/1.1" 200 None
2024-05-05 21:41:27,769 - INFO - thread_id: 2. Message: thread_id: 2. Retrieved too many records with 18000. Retrieved 10000 records.
2024-05-05 21:41:27,769 - INFO - thread_id: 2. Message: Adjusting block range to 12000, new end block: 13749431
2024-05-05 21:41:27,769 - INFO - thread_id: 2. Message: Calling Etherscan API with current_block: 13742944, ending_block: 13749431, thread_id: 2
2024-05-05 21:41:27,774 - DEBUG - Starting new HTTPS connection (1): api.etherscan.io:443
2024-05-05 21:41:28,498 - DEBUG - https://api.etherscan.io:443 "GET /api?module=account&action=txlistinternal&address=0xE592427A0AEce92De3Edee1F18E0157C05861564&startblock=13742944&endblock=13749431&page=1&offset=10000&sort=asc&apikey=H4PV22WR9MSNYJM25TN9FFXEZGB3NFDX6V HTTP/1.1" 200 None
2024-05-05 21:41:29,343 - INFO - thread_id: 2. Message: thread_id: 2. Retrieved too many records with 12000. Retrieved 10000 records.
2024-05-05 21:41:29,343 - INFO - thread_id: 2. Message: Adjusting block range to 8000, new end block: 13749431
...
module=account&action=txlistinternal&address=0xE592427A0AEce92De3Edee1F18E0157C05861564&startblock=13745145&endblock=13749431&page=1&offset=10000&sort=asc&apikey=H4PV22WR9MSNYJM25TN9FFXEZGB3NFDX6V HTTP/1.1" 200 None
2024-05-05 21:41:56,784 - INFO - thread_id: 2. Message: thread_id: 2. Retrieved too many records with 18000. Retrieved 10000 records.
2024-05-05 21:41:56,784 - INFO - thread_id: 2. Message: Adjusting block range to 12000, new end block: 13749431
2024-05-05 21:41:56,784 - INFO - thread_id: 2. Message: Calling Etherscan API with current_block: 13745145, ending_block: 13749431, thread_id: 2
2024-05-05 21:41:56,793 - DEBUG - Starting new HTTPS connection (1): api.etherscan.io:443
2024-05-05 21:42:00,911 - DEBUG - https://api.etherscan.io:443 "GET /api?module=account&action=txlistinternal&address=0xE592427A0AEce92De3Edee1F18E0157C05861564&startblock=13745145&endblock=13749431&page=1&offset=10000&sort=asc&apikey=H4PV22WR9MSNYJM25TN9FFXEZGB3NFDX6V HTTP/1.1" 200 None
2024-05-05 21:42:02,645 - INFO - thread_id: 2. Message: thread_id: 2. Retrieved too many records with 12000. Retrieved 10000 records.
2024-05-05 21:42:02,645 - INFO - thread_id: 2. Message: Adjusting block range to 8000, new end block: 13749431
2024-05-05 21:42:02,645 - INFO - thread_id: 2. Message: Calling Etherscan API with current_block: 13745145, ending_block: 13749431, thread_id: 2
2024-05-05 21:42:02,650 - DEBUG - Starting new HTTPS connection (1): api.etherscan.io:443
2024-05-05 21:42:03,917 - DEBUG - https://api.etherscan.io:443 "GET /api?module=account&action=txlistinternal&address=0xE592427A0AEce92De3Edee1F18E0157C05861564&startblock=13745145&endblock=13749431&page=1&offset=10000&sort=asc&apikey=H4PV22WR9MSNYJM25TN9FFXEZGB3NFDX6V HTTP/1.1" 200 None
2024-05-05 21:42:04,730 - INFO - thread_id: 2. Message: thread_id: 2. Retrieved too many records with 8000. Retrieved 10000 records.
2024-05-05 21:42:04,730 - INFO - thread_id: 2. Message: Adjusting block range to 4000, new end block: 13749145
2024-05-05 21:42:04,730 - INFO - thread_id: 2. Message: Calling Etherscan API with current_block: 13745145, ending_block: 13749145, thread_id: 2
2024-05-05 21:42:04,736 - DEBUG - Starting new HTTPS connection (1): api.etherscan.io:443
2024-05-05 21:42:05,482 - DEBUG - https://api.etherscan.io:443 "GET /api?module=account&action=txlistinternal&address=0xE592427A0AEce92De3Edee1F18E0157C05861564&startblock=13745145&endblock=13749145&page=1&offset=10000&sort=asc&apikey=H4PV22WR9MSNYJM25TN9FFXEZGB3NFDX6V HTTP/1.1" 200 None
2024-05-05 21:42:06,309 - INFO - thread_id: 2. Message: thread_id: 2. Retrieved too many records with 4000. Retrieved 10000 records.
2024-05-05 21:42:06,310 - INFO - thread_id: 2. Message: Adjusting block range to 2200, new end block: 13747345
2024-05-05 21:42:06,310 - INFO - thread_id: 2. Message: Calling Etherscan API with current_block: 13745145, ending_block: 13747345, thread_id: 2
2024-05-05 21:42:06,314 - DEBUG - Starting new HTTPS connection (1): api.etherscan.io:443
2024-05-05 21:42:07,087 - DEBUG - https://api.etherscan.io:443 "GET /api?module=account&action=txlistinternal&address=0xE592427A0AEce92De3Edee1F18E0157C05861564&startblock=13745145&endblock=13747345&page=1&offset=10000&sort=asc&apikey=H4PV22WR9MSNYJM25TN9FFXEZGB3NFDX6V HTTP/1.1" 200 None
2024-05-05 21:42:07,812 - INFO - thread_id: 2. Message: Etherscan API call SUCCESS! Retrieved 8171 records with a block window size of 2200
2024-05-05 21:42:12,287 - INFO - thread_id: 2. Message: Changing current block 13745145
2024-05-05 21:42:12,287 - INFO - thread_id: 2. Message: New current block 13747346
2024-05-05 21:42:12,287 - INFO - thread_id: 2. Message: Calling Etherscan API with current_block: 13747346, ending_block: 13749431, thread_id: 2
2024-05-05 21:42:12,304 - DEBUG - Starting new HTTPS connection (1): api.etherscan.io:443
2024-05-05 21:42:15,483 - DEBUG - https://api.etherscan.io:443 "GET /api?module=account&action=txlistinternal&address=0xE592427A0AEce92De3Edee1F18E0157C05861564&startblock=13747346&endblock=13749431&page=1&offset=10000&sort=asc&apikey=H4PV22WR9MSNYJM25TN9FFXEZGB3NFDX6V HTTP/1.1" 200 None
2024-05-05 21:42:16,195 - INFO - thread_id: 2. Message: Etherscan API call SUCCESS! Retrieved 7452 records with a block window size of 2200
2024-05-05 21:42:24,496 - INFO - thread_id: 2. Message: Inserted records successfully.
2024-05-05 21:42:24,503 - INFO - thread_id: 2. Message: Changing current block 13747346
2024-05-05 21:42:24,503 - INFO - thread_id: 2. Message: New current block 13749431
2024-05-05 21:42:24,503 - INFO - thread_id: 2. Message: Calling Etherscan API with current_block: 13749431, ending_block: 13749431, thread_id: 2
2024-05-05 21:42:24,506 - DEBUG - Starting new HTTPS connection (1): api.etherscan.io:443
2024-05-05 21:42:26,089 - DEBUG - https://api.etherscan.io:443 "GET /api?module=account&action=txlistinternal&address=0xE592427A0AEce92De3Edee1F18E0157C05861564&startblock=13749431&endblock=13749431&page=1&offset=10000&sort=asc&apikey=H4PV22WR9MSNYJM25TN9FFXEZGB3NFDX6V HTTP/1.1" 200 172
2024-05-05 21:42:26,409 - INFO - thread_id: 2. Message: Effing finally...Reached end of transactions for address: 0xE592427A0AEce92De3Edee1F18E0157C05861564, current_block: 13749431, ending_block: 13749431
2024-05-05 21:42:26,409 - INFO - thread_id: 2. Message: Inserted records successfully.
```

after ingestion:

```bash
postgres=# select count(1) from transactions;
  count
---------
 6226392
(1 row)

postgres=# select count(1) from addresses;
 count
--------
 598105
(1 row)
```


## Some additional annoyances

Some threads finish faster than others if we do a straight divide the work and conquer approach. Some threads finish faster because they can get through their blocks faster because.....there are more transactions on some blocks than others. Threads 0,1,2 take longer meaning there were more transctions I Think earlier for this address. Sigh... I think my approach is okay but in the future if a thread gets more than 10k, it should probably spawn a child thread and adjust. A thread spawning more threads if a limit is hit would help this heat map issue on the blocks.

## Sort

- the `sort` field in the API call if you set to `desc` will return you records in timestamp desc order, with the most recent first.
