// Import our data
// APPROACH A
import delimited "D:\Work\Dissertation\Work\Final\macrotrends-scraper\distance combined one variable method.csv", clear 


rename ebtdamargin ebtda
rename pricepairs price
rename grossprofitmargin gp
rename epsearningspersharediluted eps
rename cogsmargin cogs
rename allfundamentalvariables all

hist price, title("Histogram of price pairs")

//
//
// // ebtda margin in our data was mostly empty
// // as is evident below, so we won't be working with it
// // from this point going forward
// sum ebtda price gp eps cogs
//
// // as for the other columns, let's drop the missing rows
//
// // First, let's work with the combined value of the fundamental varaibles
// // and see how it is related with the price
// drop if missing(all) & missing(price)
//
// // Plot the relationship between teh fundamentals and the pairs
// // twoway lfit gp price, title("Price against gross profit margin") xtitle("gross profit margin") ytitle("Price") lcolor("red") || scatter  gp price, mcolor("navy%50") msize("vsmall") 
// // twoway lfit cogs price, title("Price against cost of goods sold margin") xtitle("cost of goods sold margin") ytitle("Price") lcolor("red") || scatter  cogs price, mcolor("navy%50") msize("vsmall") 
// // twoway lfit eps price, title("Price against earnings per share diluted") xtitle(" earnings per share diluted") ytitle("Price") lcolor("red") || scatter  eps price, mcolor("navy%50") msize("vsmall") 
// // twoway lfit all price, title("Price against all fundamental variables combined") xtitle("Fundamental Variables Combination") ytitle("Price") lcolor("red") || scatter  all price, mcolor("navy%50") msize("vsmall") 
//
//
// // Do Linear Regression
// reg price gp
// estimates store m1
//
// reg price cogs
// estimates store m2
//
// reg price eps
// estimates store m3
//
// reg price gp cogs
// estimates store m4
//
// reg price gp eps
// estimates store m5
//
// reg price cogs eps
// estimates store m6
//
// reg price all
// estimates store m7
//
//
//
// esttab m1 m2 m3 m4 m5 m6 m7, cells(b(star fmt(3)) se(par fmt(2)))


// // APPROACH B
// import delimited "D:\Work\Dissertation\Work\Final\macrotrends-scraper\distance combined multiple variable method.csv", clear
//
//
// rename ebtdamargin ebtda
// rename epsearningspersharediluted eps
// rename cogsmargin cogs
// rename allfundamentalvariables all
//
//
// // ebtda margin in our data was mostly empty
// // as is evident below, so we won't be working with it
// // from this point going forward
// sum ebtda eps cogs
//
// // as for the other columns, let's drop the missing rows
//
// histogram all, title("Histogram of all-fundamental-variables")
