"
11/05/22

Welcome to MUDSS' Tutorial about the R programming language!

Below are some challenges for you to complete, which will give you a flavour of what R is all about. 

Your aim is to provide some heuristics about how well we can detect a linear pattern from data at different error variances.

You will simulate data using a linear equation, then fit a model to your simulation, and evaluate the model.

We will see how the results vary for sigma = 1, 2, 3, 4, 5.

Imagine that each observation corresponds to one day, and: 
Y = average # of minutes that customers spend in a café in Manchester.
X = temperature in celsius.

"

"
Challenge 0:
Clear your environment.
"
rm(list=ls())

"
Challenge 1: 
Type in ?set.seed
This will present you with information about the set.seed() function, which we will soon invoke.
Note that you can precede any function with a '?' to learn about it.
"
?set.seed

"
Challenge 2: 
Set a seed of 10 for subsequent randomizations.
"
set.seed(10)

"
Challenge 3:
Create a vector x containing n=60 values evenly spaced between 10 and 20 (inclusive).
"
x <- seq(from=10, to=20, length.out=60)

"
Challenge 4:
Create a vector e containing n=60 values randomly sampled from an N(0,1) distribution.
"
e <- rnorm(n=60, mean=0, sd=1)

"
Challenge 5:
Create a vector y, whose i'th entry is 55 - 0.5x_i + e_i.
"
y <- 55 - 0.5*x + e

"
Challenge 6:
Fit the model Y = a + bX. Assign to variable 'model'.
"
model <- lm(y~x)

"
Challenge 7:
Plot y against x.
"
plot(x,y, pch=20, col= "turquoise")

"
Challenge 8:
Superimpose your line of best fit on the plot.
"
a <- model$coefficients[1]
b <- model$coefficients[2]
abline(a=a, b=b, col="red")
#abline(a=55, b=-0.5, col="green") if we want to compare our estimate with the true relationship.

"
Challenge 9:
Create a function that takes as input sigma (= the error variance), then:
> Creates a vector x of n values evenly spaced between 10 and 20 inclusive.
> Creates a vector e of n values randomly sampled from the N(0,3) distribution.
> Creates a vector y, whose i'th entry is 55 - 0.5x_i + e_i.
> Fits a model y = a + bx.
> Returns R^2, the coefficient of determination from the model fit.
"
fit_for_sigma <- function(sigma){
  x <- seq(from=10, to=20, length.out=60)
  e <- rnorm(n=60, mean=0, sd=sigma)
  y <- 55 - 0.5*x + e
  model <- lm(y~x)
  R2 <- summary(model)$r.squared
  return(R2)
}

"
Challenge 10:
Create a for-loop, and iterate through values sigma= 1,2,3,4, and 5 in your function.
Add the resulting R^2 values to a list.
"
R_sqds <- list()
for (sigma in 1:5){
  R2 <- fit_for_sigma(sigma)
  R_sqds <- append(R_sqds,R2)
}

"
Challenge 11:
Plot the coefficient of determination against the values of sigma. 
"
plot(x=R_sqds, y=1:5, xlab="Proportion of variation captured by the model"
     , ylab="Standard deviation of the error terms"
     , main="Randomness and model accuracy"
     , col="orange"
     , pch=18)

"
Challenge 12:
Describe what you see. Is there a general lesson we can learn here about model-fitting?
"