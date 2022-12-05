### 
In this project I was aiming to derive probabilities of fed rate hikes implied by the market participants. 

The FedFunds Futures are Traded on the CME exchange, the price of funutures for a given month is the average rate over month $\sum_{n=1}^30 100 - r_i = p$ where $r_i$s are the implied average effective fed fund rates for a given day. This can be used to forsee changes in the current target rate of the FED. 

The methodology used in order to compute implied rates is the following: 

If the FOMC meeting (announcment of the next rate target range) is on the n-th day of month, than the rate will be active for $M-N$ days, and the current effr for all days before the meeting $N$ days. Using the weighted average formula the price of futures is the following $$P = \frac{M-N}{M} * r_{after FOMC } + \frac{N}{M} * r_{before FOMC}$$. Using this formula I was able to derive the implied rate hike. The implied hike is in terms of 25 percentage poinds, however sometimes hikes are 50, 75, 100 pp. 

In order ton distinguish the binary probabilities of these higher order hikes I used the following formula $Hike_{Lower} = min(P_{hike}) * 0.25, Hike_{Higher} = Hike_{Lower} + 0.25$ 
