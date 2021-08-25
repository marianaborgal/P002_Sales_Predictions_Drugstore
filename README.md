# P002 Sales Predictions for a Drugstore Chain
**_This is a ongoing project._** <br><br>
Sales prediction for a drugstore chain.

![home](https://www.gsmmaniak.pl/wp-content/uploads/gsmmaniak/2019/03/rossmann-wypuscil-promocje-w-black-friday-ale-mocno-sie-przeliczyl-rozwscieczeni-klienci-skladaja-skargi-zwykle-zlodziejstwo-2389046.jpg) 

This repository contains codes for the sales predictions for Rossman drugstores. <br>
The data used was available on [Kaggle](https://www.kaggle.com/c/rossmann-store-sales).

#### Project 002 - Sales Predictions:
The objetives of this project are:
* Perform exploratory data analysis on sales available on dataset.
* Predict the sales for the next 6 weeks from each store of the pharmacy chain.
* Develop a online dashboard that can be acessed by the CEO from a mobile or computer.
* Develop a telegram bot that can be acessed by the CEO from a mobile or computer.

---
## 1. Business Problem
Rossmann is a pharmacy chain that operates over 3,000 stores in 7 European countries. The stores are going to be renovated and the CFO needs to know how much can be invested in each one of them. Therefore, the Data Scientist was requested to develop a sales prediction model that  forecast the sales for the next 6 weeks for each store.
<!-- Marco: This forecast also informs the CEO which store is able to account for its own restoration with the income within this period. -->

<br>The telegram bot must return:
   * The sales for the next 6 months for the given store.

## 2. Business Results
<br>
Based on business criteria, from 21,436 available properties, 10,707 should be bought by House Rocket and could result on a US$1,249,116,423.00 profit. <br>
Maximum Value Invested: US$4,163,721,410.00<br>
Maximum Value Returned: US$5,412,837,833.00<br>
Maximum Expected Profit: US$1,249,116,423.00<br>

This results on a 30.0 % gross revenue.

## 3. Business Assumptions
* The data available is only from XX to XX.
* The variables on original dataset goes as follows:<br>
Variable | Definition
------------ | -------------
|store | Unique ID for each store|
|days_of_week | |
|date | Date that the sales occurred|
|sales | Number of sales |
|customers | Number of customers |
|open | Wether the store was open (1) or closed (0)|
|promo | Wether the store was participating on a promotion (1) or not (0)|
|sate_holiday | Whether if it was a state holiday (a=public holiday, b=easter holiday, c=christmas) or not (0) |
|store_type | |
|date | |
|date | |
|date | |
|date | |

* Variables created during the project development goes as follow:

Variable | Definition
------------ | -------------
| x | xxx |


* Business criteria to determine wether a property should be bought are:
   * Property must have a 'condition' equals or bigger than 3.
   * Property price must be below or equal the median price on the region (zipcode)

<br>

## 4. Solution Strategy
1. Understanding the business model
2. Understanding the business problem
3. Collecting the data
4. Data Description
5. Data Filtering
6. Exploratory Data Analysis
7. Data Preparation
8. Feature Selection
_ongoing_
<!--
8. Exploratory Data Analysis
9. Insights Conclusion
10. Dashboard deploy on [Heroku](https://p001-realstate-insights.herokuapp.com/)-->


## 5. Top 4 Data Insights
<!--1. Properties built with basements decreased after the 80s
2. Almost 60% of the properties became available during summer/spring.
3. 50% of properties that should be bought are in a 15km radius from the lake.
4. Properties selected to be bought in a 15km radius from lake correspond to 60% of expected profit.-->

## 6. Conclusion
<!--The objective of this project was to create a online dashboard to House Rocket's CEO. Deploying the dashboard on Heroku platforms provided the CEO acess from anywhere facilitating data visualization and business decisions.-->

## 7. Next Steps
<!--* Determine which season of the year would be the best to execute a sale.
* Get more address data to fill NAs.
* Expand this methodology to other regions that House Rocket operates.-->


----
**References:**
<!--* Python from Zero to DS lessons on [Youtube](https://www.youtube.com/watch?v=1xXK_z9M6yk&list=PLZlkyCIi8bMprZgBsFopRQMG_Kj1IA1WG&ab_channel=SejaUmDataScientist)
* Blog [Seja um Data Scientist](https://sejaumdatascientist.com/os-5-projetos-de-data-science-que-fara-o-recrutador-olhar-para-voce/)
* Dataset House Sales in King County (USA) from [Kaggle](https://www.kaggle.com/harlfoxem/housesalesprediction)
* Variables meaning on [Kaggle discussion](https://www.kaggle.com/harlfoxem/housesalesprediction/discussion/207885)
* <div>Icons made by <a href="https://www.flaticon.com/authors/smashicons" title="Smashicons">Smashicons</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>-->
