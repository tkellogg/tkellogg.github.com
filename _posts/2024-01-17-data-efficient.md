---
layout: post
title: "The Unreasonable Data Efficiency of LLMs"
date: 2024-01-17
categories:
 - ai
 - LLMs
image: https://gist.github.com/assets/437044/e9443c0a-823a-46f1-82b8-ccb8a13d7111
is_draft: true
use_mermaid: false
---

Last week someone said that LLMs (Large Language Models), and the current generation of AI, weren't useful. That 
anything you can do with an LLM you could do better and more accurately with more traditional ML. 
I find that puzzling. 

On the surface, it's true. Traditional ML algorithms can be more accurate with far smaller models. But that misses a
BIG point: the data.


# Data Efficiency
I'm never quite sure what "traditional ML" means, but I assume we're talking about the era of ML models before
transformers. So [logistic regression][log], [xgboost][xgb], [deep learning][dl], [decision trees][sklearn], etc. 

Let's say we want to train a classifier. How much data does it take to train these models?

Ballpark numbers:

1. Logistic regression: 100-1,000 examples
2. Decision trees: 1,000-10,000 examples
3. XGBoost: 100-10,000 examples
4. Deep learning: 10,000-500,000 examples

We call this _**data efficiency**_: How much data do we need in order for the ML model to perform well?
As the model size & complexity increases, so does performance, and so does the number of training examples.
As you go down that list, the data efficiency drops, but the performance increases (it becomes more accurate).

There's an urban (tech) legends, like ML models in the advertising department at Target once predicted that
a woman was pregnant before she knew. They were showing her baby products a few weeks before she became aware
that she was pregnant.

Those legends, of eerily insane model performance, are what drives companies to adopt ML and AI. 


## Data Pipelines
In typical ML models used in business, the "example" tends to look a lot like a database record

| ID | Age | Zip   | LastPurchaseAmount | HasPurchasedFoodLast6Months | HasPurcha... | 
|----|-----|-------|--------------------|-----------------------------|--------------|
|  1 |  43 | 98117 |             179.35 |                        true |        false |

There's typically hundreds of columns, and a lot of one-to-many database relationships are flattened out into columns like
`HasPurchasedFoodLast6Months`. It's a very wide "table" that incorporates information from a lot of sources.
Some sources are real-time, others are batch, others are fairly static.

Wrangling enterprise data to train & execute ML models isn't easy. There's a lot of data sources, dirty data, subtly
incompatile data, etc. To deal with all this, we setup "data pipelines", basically a mess of code that flows data
through a series of steps and eventually lands it into a _feature store_, where it can be served for both training
and production inference.



# "Enhance That"
![image](https://gist.github.com/assets/437044/1b336a88-b3a3-4c86-af40-38bca95cd18b)

* Actor1: "Oh, is that him?"
* Actor2: "enhance that"
* Tech1: ...presses buttons...
* Actor1: "We got him!"
* My dad: Noooo! you can't just create information out of nothing!

I'm sure you've seen that scene before, in some cop show. My dad is right, if the picture is too grainy to see, you
can't simply "enhance" it into clarity. The information, the detail, doesn't exist in the file.




 [log]: https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression
 [xgb]: https://xgboost.readthedocs.io/en/stable/
 [dl]: https://pytorch.org/
 [sklearn]: https://scikit-learn.org/stable/modules/tree.html
