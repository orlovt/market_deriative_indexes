### Idea

In this project I was aiming to derive probabilities of fed rate hikes implied by the market participants simularly to [**CME's FedWatchTool**](https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html) 

### Data Source 

The **Fed Funds Futures** are Traded on the [**CME**](https://www.cmegroup.com "The link to exchange") exchange, the price of futures for a given month is the average rate over month $\small{\sum_{n=1}^{30} 100 - r_i}$,  where $\small{r_i}$ is the implied *effective fed fund rate* for a given day. This data be used  can be used to forsee changes in the current target rate of the FED. The Effective fed funds rate was parsed from [*St. Louis FRED*](https://fred.stlouisfed.org/series/EFFR)



### CMEs methodology 
The methodology provided on the [*CME's website*](https://www.cmegroup.com/education/demos-and-tutorials/fed-funds-futures-probability-tree-calculator.html) lacks transparency and is incomplete. For the most part the examples are trivial (no hike or 25 basis point hike), the formulas to compiute variables are poorly defined. 



### Methodology used

The methodology used in order to compute implied probabilities of rate hikes is the following: 

- If the FOMC meeting (announcment of the next rate target range) is on the n-th day of month, than the rate will be active for $\small{M-N}$ days, and the current EFFR(Effective Fed Funds Rate) for all days before the meeting ($\small{N}$ days). 

- Using the weighted average formula the price of futures is the following $\large{P = \frac{M-N}{M} * r_{t+1} + \frac{N}{M} * r_{t}}$,where $\small{r_{t+1}}$ is the rate after the FOMC meeting and $\small{r_{t}}$ is the rate before one. 

 - Using this formula I was able to derive the implied rate hike. The implied hike is in terms of 25 percentage poinds, however sometimes hikes are 50, 75, 100 percentage points. 

In order to distinguish the binary probabilities of these higher order hikes (50pp vs. 75pp for example), I used the following formula $\small{H_{Lower} = rounddown(P_{hike}) * 0.25, H_{Higher} = H_{Lower} + 0.25}$, these are representatve of the actuall implied probabilities, due to the nature of futurres pricing. With this the case for da

### Use cases? 

1. Can show the convergance of the implied probailities of rate hikes. 

2. Can show shock in the expectations for the Fed Funds Rate.  

### What was achived? 

