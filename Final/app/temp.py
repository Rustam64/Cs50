import re

coupang_id = "https://www.coupang.com/vp/products/8242925355?itemId=20648620282&vendorItemId=90627073123&q=dark+spot&itemsCount=36&searchId=154895ac2654474&rank=2&searchRank=2&isAddedCart="
pattern = r"\/(\d+\?itemId=\d+\&vendorItemId=\d+)"
match = re.search(pattern, coupang_id)
if match:
    print(match.group(1))
