# from fu yao's chain of thought hub
math_examples='''Question: 
What is the largest value of $x$ such that the expression \[\dfrac{x+1}{8x^2-65x+8}\] is not defined?
Let's think step by step.
Answer: 
In this particular case, the fraction will be undefined only if its denominator is equal to zero. 
Because of this, we can ignore the numerator. 
We start by setting the binomial in the denominator equal to 0: 
\begin{align*} 8x^2-65x+8=0
\\\Rightarrow\qquad (8x-1)(x-8)=0
\end{align*} 
We find that the two possible values for $x$ are $\frac18$ and $8$. 
Since the question asks for the largest value, the final solution is $\boxed{8}$.
[ANSWERKEY] 8

Question: 
BoatWorks built 3 canoes in January of this year and then each subsequent calendar month they built twice the number of canoes they had built the previous month. How many total canoes were built by BoatWorks by the end of March of this year?
Let's think step by step.
Answer: 
The number of boats built is $3+3\cdot2+3\cdot2^2 = 3+6+12 = \boxed{21}$.
[ANSWERKEY] 21

Question: 
If $5a+2b=0$ and $a$ is two less than $b$, what is $7b$?
Let's think step by step.
Answer: 
First we begin by solving the system of equations \begin{align*}
5a+2b&=0, \\
b-2&=a.
\end{align*}
Making the substitution for $a$ from the second equation to the first, we get $5(b-2)+2b=0$, 
which simplifies to $7b-10=0$. 
Solving for $b$, we find that $b=\frac{10}{7}$. 
Hence $7b=7\cdot \frac{10}{7}=\boxed{10}$.
[ANSWERKEY] 10

Question: 
The difference between two numbers is 9, and the sum of the squares of each number is 153. What is the value of the product of the two numbers?
Let's think step by step.
Answer: 
Call the first number $x$ and the second number $y$. 
Without loss of generality, assume $x > y$. 
We can represent the information given in the problem with the following system of linear equations:
\begin{align*}
x - y &= 9\\
x^2 + y^2 &= 153
\end{align*} 
Solving for $x$ in the first equation and substituting into the second yields $(9+y)^2 + y^2 = 153$, or $2y^2 + 18y - 72 = 0$. 
Canceling a $2$ gives $y^2 + 9y - 36 = 0$, which factors into $(y+12)(y-3)$. 
Thus, $y = 3$ and $x = 12$. So, $x \cdot y = \boxed{36}$.
[ANSWERKEY] 36

Question: 
Simplify $\frac{1}{1+\sqrt{2}}\cdot\frac{1}{1-\sqrt{2}}$.
Let's think step by step.
Answer: 
Multiplying the numerators simply yields $1$. 
Multiplying the denominators gives $1+\sqrt{2} - \sqrt{2} -2 = 1 - 2 = -1$. 
So, the answer is $\frac{1}{-1} = \boxed{-1}$.
[ANSWERKEY] -1

Question: 
Four people can mow a lawn in 6 hours. How many more people will be needed to mow the lawn in 4 hours, assuming each person mows at the same rate?
Let's think step by step.
Answer: 
The number of people mowing and the time required to mow are inversely proportional. 
Letting $n$ be the number of people and $t$ be the amount of time, we have $nt = (4)(6)= 24$ 
because 4 people can mow a lawn in 6 hours. 
If $m$ people can mow the lawn in 4 hours, then we must have $m(4) = 24$, so $m=6$.  
Therefore, we need $6-4 = \boxed{2}$ more people to complete the job in 4 hours.
[ANSWERKEY] 2

Question: 
BoatsRUs built 7 canoes in January of this year and then each subsequent calendar month they built twice the number of canoes they had built the previous month. How many total canoes were built by BoatsRUs by the end of May of this year?
Let's think step by step.
Answer: 
The numbers of canoes built by BoatsRUs each month form a geometric sequence: 7, 14, 28, 56, 112. 
The first term is 7 and the common ratio is 2, so the sum of these terms is $\frac{7(2^5-1)}{2-1} = \boxed{217}$.
[ANSWERKEY] 217

Question: 
Find the coefficient of the $x^2$ term in the expansion of the product $(ax^3 + 3x^2 - 2x)(bx^2 - 7x - 4)$.
Let's think step by step.
Answer:
We only need to worry about the terms that multiply to have a degree of $2$. 
This would be given by the product of the terms $3x^2$ and $-4$ as well as the product of the terms $-2x$ and $-7x$. 
Thus, $$(3x^2) \times (-4) + (-2x) \times (-7x) = -12x^2 + 14x^2 = 2x^2,$$and the coefficient is $\boxed{2}$.
[ANSWERKEY] 2

'''