from collections import deque
import math
import copy

liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}

def swapExactTokensForTokens(amount_in, reserve_in, reserve_out):
    fee = 997
    amount_in_with_fee = amount_in * fee / 1000
    numerator = amount_in_with_fee * reserve_out
    denominator = reserve_in + amount_in_with_fee
    amount_out = numerator / denominator

    return amount_out

def find_shortest_arbitrage_path(start_token, target_amount, liquidity, initial_amount):
    queue = deque([(start_token, initial_amount, [], [])])  # (current_token, current_amount, path, swap_details)
    while queue:
        current_token, current_amount, path, swap_details = queue.popleft()
        if current_token == start_token and len(path) > 0 and current_amount >= target_amount:
            return path, swap_details, current_amount

        for (from_token, to_token), reserves in liquidity.items():
            if (from_token == current_token or to_token == current_token) and (from_token, to_token) not in path:
                if from_token == current_token:
                    amount_out = swapExactTokensForTokens(current_amount, reserves[0], reserves[1])
                    next_token = to_token
                    extended_swap_details = swap_details + [(current_amount, amount_out)]
                    
                else:
                    amount_out = swapExactTokensForTokens(current_amount, reserves[1], reserves[0])
                    next_token = from_token
                    extended_swap_details = swap_details + [(current_amount, amount_out)]
                extended_path = path + [(current_token, next_token)]

                queue.append((next_token, amount_out, extended_path, extended_swap_details))

    return None

start_token = 'tokenB'
initial_amount = 5
target_amount = 20

arbitrage_result = find_shortest_arbitrage_path(start_token, target_amount, liquidity, initial_amount)

if arbitrage_result:
    path, swap_details, final_balance = arbitrage_result
    print("Profitable path:")
    for i, swap in enumerate(path):
        print(f"{swap[0]} -> {swap[1]}, amountIn: {swap_details[i][0]}, amountOut: {swap_details[i][1]}")

    path_str = start_token

    for (from_token, to_token) in path:
        if from_token == start_token or to_token == start_token:
            if from_token == start_token:
                path_str += f"->{to_token}"
                start_token = to_token 
            else:
                path_str += f"->{from_token}"
                start_token = from_token

    print(f"path: {path_str}, {start_token} balance={final_balance}")

else:
    print("No profitable arbitrage path found.")
