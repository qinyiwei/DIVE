gsm8k_examples = '''Question: Angelo and Melanie want to plan how many hours over the next week they should study together for their test next week. They have 2 chapters of their textbook to study and 4 worksheets to memorize. They figure out that they should dedicate 3 hours to each chapter of their textbook and 1.5 hours for each worksheet. If they plan to study no more than 4 hours each day, how many days should they plan to study total over the next week if they take a 10-minute break every hour, include 3 10-minute snack breaks each day, and 30 minutes for lunch each day?
Let's think step by step.
Answer:
Angelo and Melanie think they should dedicate 3 hours to each of the 2 chapters, 3 hours x 2 chapters = 6 hours total.
For the worksheets they plan to dedicate 1.5 hours for each worksheet, 1.5 hours x 4 worksheets = 6 hours total.
Angelo and Melanie need to start with planning 12 hours to study, at 4 hours a day, 12 / 4 = 3 days.
However, they need to include time for breaks and lunch. Every hour they want to include a 10-minute break, so 12 total hours x 10 minutes = 120 extra minutes for breaks.
They also want to include 3 10-minute snack breaks, 3 x 10 minutes = 30 minutes.
And they want to include 30 minutes for lunch each day, so 120 minutes for breaks + 30 minutes for snack breaks + 30 minutes for lunch = 180 minutes, or 180 / 60 minutes per hour = 3 extra hours.
So Angelo and Melanie want to plan 12 hours to study + 3 hours of breaks = 15 hours total.
They want to study no more than 4 hours each day, 15 hours / 4 hours each day = 3.75
They will need to plan to study 4 days to allow for all the time they need.
[ANSWERKEY] 4

Question: Mark's basketball team scores 25 2 pointers, 8 3 pointers and 10 free throws.  Their opponents score double the 2 pointers but half the 3 pointers and free throws.  What's the total number of points scored by both teams added together?
Let's think step by step.
Answer:
Mark's team scores 25 2 pointers, meaning they scored 25*2= 50 points in 2 pointers.
His team also scores 6 3 pointers, meaning they scored 8*3= 24 points in 3 pointers
They scored 10 free throws, and free throws count as one point so they scored 10*1=10 points in free throws.
All together his team scored 50+24+10= 84 points
Mark's opponents scored double his team's number of 2 pointers, meaning they scored 50*2=100 points in 2 pointers.
His opponents scored half his team's number of 3 pointers, meaning they scored 24/2= 12 points in 3 pointers.
They also scored half Mark's team's points in free throws, meaning they scored 10/2=5 points in free throws.
All together Mark's opponents scored 100+12+5=117 points
The total score for the game is both team's scores added together, so it is 84+117=201 points
[ANSWERKEY] 201

Question: Bella has two times as many marbles as frisbees. She also has 20 more frisbees than deck cards. If she buys 2/5 times more of each item, what would be the total number of the items she will have if she currently has 60 marbles?
Let's think step by step.
Answer:
When Bella buys 2/5 times more marbles, she'll have increased the number of marbles by 2/5*60 = 24
The total number of marbles she'll have is 60+24 = 84
If Bella currently has 60 marbles, and she has two times as many marbles as frisbees, she has 60/2 = 30 frisbees.
If Bella buys 2/5 times more frisbees, she'll have 2/5*30 = 12 more frisbees.
The total number of frisbees she'll have will increase to 30+12 = 42
Bella also has 20 more frisbees than deck cards, meaning she has 30-20 = 10 deck cards
If she buys 2/5 times more deck cards, she'll have 2/5*10 = 4 more deck cards.
The total number of deck cards she'll have is 10+4 = 14
Together, Bella will have a total of 14+42+84 = 140 items
[ANSWERKEY] 140

Question: A group of 4 fruit baskets contains 9 apples, 15 oranges, and 14 bananas in the first three baskets and 2 less of each fruit in the fourth basket. How many fruits are there?
Let's think step by step.
Answer:
For the first three baskets, the number of apples and oranges in one basket is 9+15=24
In total, together with bananas, the number of fruits in one basket is 24+14=38 for the first three baskets.
Since there are three baskets each having 38 fruits, there are 3*38=114 fruits in the first three baskets.
The number of apples in the fourth basket is 9-2=7
There are also 15-2=13 oranges in the fourth basket
The combined number of oranges and apples in the fourth basket is 13+7=20
The fourth basket also contains 14-2=12 bananas.
In total, the fourth basket has 20+12=32 fruits.
The four baskets together have 32+114=146 fruits.
[ANSWERKEY] 146

'''

# from fu yao's chain of thought hub
# gsm8k_examples = '''Question:
# Ivan has a bird feeder in his yard that holds two cups of birdseed. Every week, he has to refill the emptied feeder. Each cup of birdseed can feed fourteen birds, but Ivan is constantly chasing away a hungry squirrel that steals half a cup of birdseed from the feeder every week. How many birds does Ivan's bird feeder feed weekly?
# Answer:
# Let's think step by step.
# The squirrel steals 1/2 cup of birdseed every week, so the birds eat 2 - 1/2 = 1 1/2 cups of birdseed.
# Each cup feeds 14 birds, so Ivan's bird feeder feeds 14 * 1 1/2 = 21 birds weekly.
# [ANSWERKEY] 21

# Question:
# Samuel took 30 minutes to finish his homework while Sarah took 1.3 hours to finish it. How many minutes faster did Samuel finish his homework than Sarah?
# Answer:
# Let's think step by step.
# Since there are 60 minutes in 1 hour, then 1.3 hours is equal to 1.3 x 60 = <<1.3*60=78>>78 minutes.
# Thus, Samuel is 78 - 30 = <<78-30=48>>48 minutes faster than Sarah.
# [ANSWERKEY] 48

# Question:
# Julia bought 3 packs of red balls, 10 packs of yellow balls, and 8 packs of green balls. There were 19 balls in each package. How many balls did Julie buy in all?
# Answer:
# Let's think step by step.
# The total number of packages is 3 + 10 + 8 = <<3+10+8=21>>21.
# Julia bought 21 * 19 = <<21*19=399>>399 balls.
# [ANSWERKEY] 399

# Question:
# Lexi wants to run a total of three and one-fourth miles. One lap on a particular outdoor track measures a quarter of a mile around. How many complete laps must she run?
# Answer:
# Let's think step by step.
# There are 3/ 1/4 = 12 one-fourth miles in 3 miles.
# So, Lexi will have to run 12 (from 3 miles) + 1 (from 1/4 mile) = <<12+1=13>>13 complete laps.
# [ANSWERKEY] 13

# Question:
# Asia bought a homecoming dress on sale for $140. It was originally priced at $350. What percentage off did she get at the sale?
# Answer:
# Let's think step by step.
# Asia saved $350 - $140 = $<<350-140=210>>210 on the dress.
# That means she saved $210 / $350 = <<210/350=0.60>>0.60 or 60% off on the dress.
# [ANSWERKEY] 60

# Question:
# As a special treat, Georgia makes muffins and brings them to her students on the first day of every month.  Her muffin recipe only makes 6 muffins and she has 24 students.  How many batches of muffins does Georgia make in 9 months?
# Answer:
# Let's think step by step.
# She has 24 students and her muffin recipe only makes 6 muffins so she needs to bake 24/6 = <<24/6=4>>4 batches of muffins
# She brings muffins on the 1st of the month for 9 months and it takes 4 batches to feed all of her students so she bakes 9*4 = 36 batches of muffins
# [ANSWERKEY] 36

# Question:
# Jorge bought 24 tickets for $7 each. For purchasing so many, he is given a discount of 50%. How much, in dollars, did he spend on tickets?
# Answer:
# Let's think step by step.
# Jorge spent 24 tickets * $7 per ticket = $<<24*7=168>>168 total.
# After applying the discount, Jorge spent $168 * 0.50 = $<<168*0.50=84>>84.
# [ANSWERKEY] 84

# Question:
# OpenAI runs a robotics competition that limits the weight of each robot. Each robot can be no more than twice the minimum weight and no less than 5 pounds heavier than the standard robot. The standard robot weighs 100 pounds. What is the maximum weight of a robot in the competition?
# Answer:
# Let's think step by step.
# The minimum is 5 more than 100 so 100+5=<<100+5=105>>105.
# The maximum weight of a robot is twice the minimum 105*2=<<105*2=210>>210.
# [ANSWERKEY] 210

# '''