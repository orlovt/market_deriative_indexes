## IDEA

In this project I was aiming to derive probabilities of fed rate hikes implied by the market participants simularly to CME's FedWatchTool + add link 

## Data

The **Fed Funds Futures** are Traded on the **CME** exchange, the price of futures for a given month is the average rate over month $\small{\sum_{n=1}^{30} 100 - r_i}$,  where $\small{r_i}$ is the implied *effective fed fund rate* for a given day. This data be used  can be used to forsee changes in the current target rate of the FED. 

## Methodology

The methodology used in order to compute implied rates is the following: 

If the FOMC meeting (announcment of the next rate target range) is on the n-th day of month, than the rate will be active for $M-N$ days, and the current effr for all days before the meeting $N$ days. Using the weighted average formula the price of futures is the following $\large{P = \frac{M-N}{M} * r_{t+1} + \frac{N}{M} * r_{t}}$,where $\small{r_{t+1}}$ is the rate after the FOMC meeting and $\small{r_{t}}$ is the rate before one. 

 Using this formula I was able to derive the implied rate hike. The implied hike is in terms of 25 percentage poinds, however sometimes hikes are 50, 75, 100 percentage points. 

In order ton distinguish the binary probabilities of these higher order hikes (50pp vs. 75pp for example), I used the following formula $H_{Lower} = min(P_{hike}) * 0.25, H_{Higher} = H_{Lower} + 0.25$, these are representatve of the actuall implied probabilities, due to the nature of futurres pricing. 

## How to use? 

