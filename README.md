# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/f062f0a3-171d-4c20-8f97-7305b7638cf5/ee11842c-bef4-4a3d-9a69-77ec1ad388c8/Untitled.png)

## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

滑點指的是交易預期價格與實際執行價格之間的差異。 滑點發生的原因是流動性池內供需變化影響了價格，尤其是當大額交易相對於池子大小時，價格變化會更加顯著。

Uniswap V2 使用恆定乘積公式 (x * y = k) 來維持流動性池的平衡。 為了處理滑點，它允許用戶指定他們願意接受的交易的最小輸出代幣量，這在交易中被稱為 `amountOutMin`。 這個機制透過確保交易在使用者可接受的滑點範圍內執行，或在超出這個範圍時失敗，來保護使用者免受過度滑點的影響。

```solidity
function swapExactTokensForTokens(
    uint256 amountIn,
    uint256 amountOutMin,
    address[] path,
    address to,
    uint256 deadline
) public returns (uint256[] memory amounts) {
    require(deadline >= block.timestamp, "UniswapV2: EXPIRED");
    amounts = getAmountsOut(amountIn, path);
    require(amounts[amounts.length - 1] >= amountOutMin, "UniswapV2: INSUFFICIENT_OUTPUT_AMOUNT");

    transferTokens(path[0], amounts[0], path[1]);
    for (uint i; i < path.length - 1; i++) {
        (address input, address output) = (path[i], path[i + 1]);
        (uint reserveIn, uint reserveOut) = getReserves(input, output);
        uint amountOut = getAmountOut(amounts[i], reserveIn, reserveOut);

        transferTokens(output, amountOut, path[i + 2]);
    }
    return amounts;
}

function getAmountOut(uint amountIn, uint reserveIn, uint reserveOut) public pure returns (uint amountOut) {
    require(amountIn > 0, "UniswapV2: INSUFFICIENT_INPUT_AMOUNT");
    require(reserveIn > 0 && reserveOut > 0, "UniswapV2: INSUFFICIENT_LIQUIDITY");
    uint amountInWithFee = amountIn * 997;
    uint numerator = amountInWithFee * reserveOut;
    uint denominator = (reserveIn * 1000) + amountInWithFee;
    amountOut = numerator / denominator;
}
```

`swapExactTokensForTokens`函數執行代幣交換，並確保實際輸出量大於或等於 `amountOutMin`，否則交易將被revert。

## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

- 防止除以零錯誤：當流動性池第一次創建時，如果沒有扣除最小流動性，那麼任何小額交易都可能導致極大的價格波動，因為流動性池的代幣數量非常少，甚至可能導致除以零的錯誤
- 確保價格有意義：在流動性池第一次創建時，如果流動性提供者收到與他們提供的資產完全對等的流動性代幣，那這些代幣的價格將是無限的。
- 增加池子的穩定性：扣除的最小流動性代表池中永久鎖定的資產，有助於增加池子的穩定性和抵抗小額攻擊的能力。

## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

在 Uniswap V2Pair 合約中的 mint 函數裡，當存入代幣進行流動性提供（非首次）時，用戶獲得的流動性是透過一個特定公式計算的。 這個公式是為了確保流動性的分配與存入的資金比例相匹配，並且保持流動性池的恆定乘積公式
$x×y=k$ 

確保新的流動性提供者獲得的流動性代幣數量與其對池子的貢獻成比例。透過這個公式，Uniswap 可以維護流動性代幣的價值，也幫助維持市場的效率和流動性，確保價格不會因為流動性的增加或減少而產生不合理的波動。

## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?

Sandwich Attack是常見的一種攻擊方式，特別是在AMM如 Uniswap 上進行代幣交換時。這種攻擊發生在當攻擊者在目標交易前後執行兩個交易，以利用受害者交易的市場影響。

前額交易：攻擊者監測交易池等待大額交易出現。 當攻擊者發現一個大額交易準備發生時，他們會先於受害者的交易執行一個買入交易，以增加目標代幣的價格。

受害者交易：受害者的交易隨後發生，因為市場價格已被攻擊者的前額交易抬高，受害者將以更高的價格購買目標代幣。

後置交易：受害者交易後，攻擊者執行賣出交易，出售他們之前以較低價格買入的代幣，由於受害者交易的市場影響，攻擊者可以以較高價格賣出，從而獲得利潤。

影響：
受害者會遭受更高的滑點，因為他們的交易在攻擊者提高價格後執行。由於價格被人為抬高，受害者支付的代價會比市場正常價格更高。
受害者將因價格被操縱而獲得較少的輸出代幣，降低了他們的資本效率。
