// Import our data
import delimited "D:\Work\Dissertation\Work\Final\macrotrends-scraper\distance combined one variable method.csv", clear 


rename pricepairs price
rename grossprofitmargin gp
rename epsearningspersharediluted eps
rename cogsmargin cogs


// ebtda margin in our data was mostly empty
// as is evident below, so we won't be working with it
// from this point going forward
sum ebtdamargin grossprofitmargin cogsmargin epsearningspersharediluted allfundamentalvariables pricepairs

// as for the other columns, let's drop the missing rows

// First, let's work with the combined value of the fundamental varaibles
// and see how it is related with the price
drop if missing(allfundamentalvariables) & missing(pricepairs)

// Plot the relationship between teh fundamentals and the pairs
twoway lfit grossprofitmargin pricepairs, title("Price against gross profit margin") xtitle("gross profit margin") ytitle("Price") lcolor("red") || scatter  grossprofitmargin pricepairs, mcolor("navy%50") msize("vsmall") 
twoway lfit cogsmargin pricepairs, title("Price against cost of goods sold margin") xtitle("cost of goods sold margin") ytitle("Price") lcolor("red") || scatter  cogsmargin pricepairs, mcolor("navy%50") msize("vsmall") 
twoway lfit epsearningspersharediluted pricepairs, title("Price against earnings per share diluted") xtitle(" earnings per share diluted") ytitle("Price") lcolor("red") || scatter  epsearningspersharediluted pricepairs, mcolor("navy%50") msize("vsmall") 
twoway lfit allfundamentalvariables pricepairs, title("Price against all fundamental variables combined") xtitle("Fundamental Variables Combination") ytitle("Price") lcolor("red") || scatter  pricepairs allfundamentalvariables, mcolor("navy%50") msize("vsmall") 


// Do Linear Regression
reg pricepairs grossprofitmargin
estimates store m1

reg pricepairs cogsmargin
estimates store m2

reg pricepairs epsearningspersharediluted
estimates store m3

reg pricepairs allfundamentalvariables
estimates store m6

reg pricepairs grossprofitmargin cogsmargin
estimates store m4

reg pricepairs grossprofitmargin epsearningspersharediluted
estimates store m5

reg pricepairs cogsmargin epsearningspersharediluted
estimates store m6

reg pricepairs grossprofitmargin cogsmargin epsearningspersharediluted
estimates store m7



esttab m1 m2 m3 m4 m5 m6 m7, cells(b(star fmt(3)) se(par fmt(2)))
