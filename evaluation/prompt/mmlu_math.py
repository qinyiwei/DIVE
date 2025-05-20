mmlu_math_examples='''Question: 
Find the degree for the given field extension Q(sqrt(2), sqrt(3), sqrt(18)) over Q.\n\nYou are provided with the following options for your answer:\nA. 0\nB. 4\nC. 2\nD. 6
Let's think step by step.
Answer: 
1. $ \sqrt{18} = \sqrt{2} \cdot \sqrt{3} $, so $Q(\sqrt{2}, \sqrt{3}, \sqrt{18})$ is equivalent to $Q(\sqrt{2}, \sqrt{3})$.
2. $Q(\sqrt{2})$ over $Q$ has degree 2 because $\sqrt{2}$ is a root of the irreducible polynomial $x^2 - 2$.
3. $Q(\sqrt{3})$ over $Q$ has degree 2 because $\sqrt{3}$ is a root of the irreducible polynomial $x^2 - 3$.
4. Since the extensions $Q(\sqrt{2})$ and $Q(\sqrt{3})$ are independent, the degree of the composite extension $Q(\sqrt{2}, \sqrt{3})$ is the product of the individual degrees, which is $2 \times 2 = 4$.
Therefore, the correct answer is: B
[ANSWERKEY] B

Question: 
If 3 cans of pears cost $2.37 how many cans of pears can you buy for $9.48?\n\nYou are provided with the following options for your answer:\nA. 3 cans\nB. 12 cans\nC. 36 cans\nD. 13 cans
Let's think step by step.
Answer: 
Given that 3 cans of pears cost $2.37, we can find the cost per can by dividing the total cost by the number of cans:
Cost per can = $2.37 / 3
Now, we can use the cost per can to determine how many cans you can buy for $9.48:
Number of cans = Total budget / Cost per can
Number of cans = $9.48 / (Cost per can)
Let's calculate the cost per can first:
Cost per can = $2.37 / 3 ≈ $0.79 per can
Now, let's find the number of cans you can buy for $9.48:
Number of cans = $9.48 / $0.79 ≈ 12 cans
So, the correct answer is:
B. 12 cans
[ANSWERKEY] B

Question: 
Solve for the sum of all possible values of $x$ when $3^{x^2+4x+4}=9^{x+2}$.\n\nYou are provided with the following options for your answer:\nA. 1\nB. 2\nC. -2\nD. 0
Let's think step by step.
Answer: 
The given equation is $3^{x^2 + 4x + 4} = 9^{x+2}$.
We know that $9$ can be expressed as $3^2$. So, let's rewrite the equation using this information:
\[3^{x^2 + 4x + 4} = (3^2)^{x+2}\]
Now, we can use the property that $a^{mn} = (a^m)^n$:
\[3^{x^2 + 4x + 4} = 3^{2(x+2)}\]
Since the bases are the same, we can equate the exponents:
\[x^2 + 4x + 4 = 2(x+2)\]
Now, simplify and solve for $x$:
\[x^2 + 4x + 4 = 2x + 4\]
Subtract $2x + 4$ from both sides:
\[x^2 + 2x = 0\]
Factor out $x$:
\[x(x + 2) = 0\]
So, the possible values for $x$ are $x = 0$ or $x = -2$.
Now, let's find the sum of all possible values of $x$:
\[0 + (-2) = -2\]
So, the correct answer is:
C. -2
C [ANSWERKEY] C

'''
