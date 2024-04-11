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
    amount_in_with_fee = amount_in * fee
    numerator = amount_in_with_fee * reserve_out
    denominator = (1000*reserve_in) + amount_in_with_fee
    amount_out = numerator / denominator

     # 计算交易前的K值
    k_before = reserve_in * reserve_out
    # Update liquidity pools
    new_reserve_in = reserve_in + amount_in_with_fee/1000
    new_reserve_out = reserve_out - amount_out
    # 计算交易后的K值
    k_after = new_reserve_in * new_reserve_out

    if math.isclose(k_before, k_after, rel_tol=1e-9):
        pass
    else:
        print("K value changed: before = {}, after = {}".format(k_before, k_after))

    return amount_out, new_reserve_in, new_reserve_out


def find_shortest_arbitrage_path(start_token, target_amount, liquidity):
    queue = deque([(start_token, initial_amount, [], 0)])  # (current_token, current_amount, path, depth)
    visited = set()

    while queue:
        current_token, current_amount, path, depth = queue.popleft()
        if current_token == start_token and current_amount >= target_amount and depth > 0:
            return path, current_amount

        for (from_token, to_token), reserves in liquidity.items():
            if from_token == current_token or to_token == current_token:
                if from_token == current_token and (from_token, to_token) not in visited:
                    amount_out, _, _ = swapExactTokensForTokens(current_amount, reserves[0], reserves[1])
                    next_token = to_token
                elif to_token == current_token and (to_token, from_token) not in visited:
                    amount_out, _, _ = swapExactTokensForTokens(current_amount, reserves[1], reserves[0])
                    next_token = from_token
                else:
                    continue

                visited.add((from_token, to_token))  # Mark this transition as visited
                extended_path = path + [f"{next_token}"]
                queue.append((next_token, amount_out, extended_path, depth + 1))

    return None

start_token = 'tokenB'
initial_amount = 5
target_amount = 20

# 使用广度优先搜索寻找最短套利路径
arbitrage_result = find_shortest_arbitrage_path(start_token, target_amount, liquidity)

if arbitrage_result:
    path, final_amount = arbitrage_result
    print(f"Profitable path: {'->'.join(path)}, {start_token} balance={final_amount}")
    for i, swap in enumerate(path):
        print(f"{swap[0]} -> {swap[1]}, amountIn: {swap_details[i][0]}, amountOut: {swap_details[i][1]}")
else:
    print("No profitable arbitrage path found.")
