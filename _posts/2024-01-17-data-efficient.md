---
layout: post
title: "The Unreasonable Data Efficiency of LLMs"
date: 2024-01-17 15:00:00 +0000
categories:
 - ai
 - llms
 - machine-learning
 - data-science
 - compression
 - privacy
 - cost-optimization
 - embeddings
image: https://gist.github.com/assets/437044/e9443c0a-823a-46f1-82b8-ccb8a13d7111
is_draft: true
use_mermaid: false
---

One very cool and under-appreciated thing about machine learning (ML) and especially large language models 
(LLMs) is how they compress knowledge and unleash it in ways that feel like magic. Things that didn't seem
possible a few years ago are now somehow commodities. The thing is, it's far more than that. I argue they'll
help solve a lot of cost overruns and privacy breaches that are common in IT systems.


# "Enhance That"
Have you ever watched some cop thriller where the main characters are searching security video footage
for evidence and they think they found something but can't quite make it out, so they zoom into the grainy
video and the image becomes clear?

![image](https://gist.github.com/assets/437044/1b336a88-b3a3-4c86-af40-38bca95cd18b)

* Actor1: "Oh, is that him?"
* Actor2: "enhance that"
* Tech1: ...presses buttons...
* Actor1: "We got him!"
* _My dad: Noooo! you can't just create information out of nothing!_

My dad has a point. On the surface, you can't just _zoom in_, that would be tantamount to creating information
where there previously was no information. It breaks the laws of physics.

> The fundamental problem of communication is that of reproducing at one point either exactly or approximately a message selected at another point. Frequently the messages have meaning; that is they refer to or are correlated according to some system with certain physical or conceptual entities. These semantic aspects of communication are irrelevant to the engineering problem. The significant aspect is that the actual message is one selected from a set of possible messages. The system must be designed to operate for each possible selection, not just the one which will actually be chosen since this is unknown at the time of design.
>
> **Claude Shannon, _"A Mathematical Theory of Communication"_**

And yet, we have this technology. 

## Picture A Black Hole

In 2017 the [Event Horizon Telescope][eht] took a picture of a black hole in a faraway galaxy, 55 million light-years
away. The pictures are mesmerizing. The problem is that the picture is also impossible.

![picture of black hole taken by the Event Horizon Telescope](https://www.science.org/do/10.5555/article.2476085/full/sf-M87blackhole-1644894886423.jpg)

The problem is that it would take a radio dish larger than Earth to take that photo, and I know that didn't
happen. Instead, NASA invented a machine learning algorithm called [PRIMO][PRIMO]. They trained it on lots
of other photos of objects around the universe. That enabled them to take several real photos from around
the globe and stitch them together to provide an accurate depiction of what the black hole looks like.

That's super cool, right?


# ML is Compression
Why does this work? You can't create information where there is none, right?

Right! But you can acquire information out of band.

Think about the security cam footage. A lot of people can look at a grainy picture and squint hard to "see"
objects in the picture. It's the same thing. They have a lot of general life experience with looking
at faces, people, and other objects that might show up on a security camera, and they make a guess.
They're not creating information, they're using **_out-of-band_ information**.

You can train a machine learning algorithm on lots of pictures from security camera footage and it'll learn
what can be expected. Eventually, after it's seen enough pictures, it'll seem like it's able to enhance
a picture to "zoom in". It's not creating information, it's using it's "experience" to guess what's between
the granulated pixels.

![text](https://miro.medium.com/v2/resize:fit:720/format:webp/1*RxuQz8chZmHk8n2fwpgDsg.png)

It's fairly well known that [ML is compression][boykis]. In fact, someone used [stable diffusion to compress
images][compress]. The decompressed version wasn't perfect according to the standard metrics, but in a lot
of ways it felt like the image quality actually improved from the original.

Whoah. Un-lossless comression?

Essentially, when the model is trained, it memorizes "features" of objects. It knows what faces look like,
it just has to remember what's unique about _**this**_ face. That's a lot less information to remember.

# LLMs Are Higher Order ML
When you ask an LLM a question or to perform some task, it [creates an ML model][svm] (an SVM) and then
uses it to carry out the task you requested. So an LLM is basically a giant ML model with the majority of human 
knowledge compressed inside it, that generates other micro-purposed ML models tailored to your specific
problem.

I like to think of it as "higher order ML", but most people just call it in-context learning. It's this
"ML is compression" principal taken to the max.

# Putting it into Action
All ML is compression, but LLMs are especially good because they're trained on truly massive amounts of
text from all over the internet. As a result, we have things like 1-shot learning (or 5-shot, 10-shot, etc.),
where you can create an "ML algorithm" out of an LLM prompt with only 1 training example (or 5, 10, etc.).

For those who haven't been following ML for years, this is crazy:

![image](https://gist.github.com/assets/437044/7aadcd4a-21d5-4dea-9126-d0e339e71828)

The "ML algorithm" built on an LLM requires **magnitudes** less data, like 100x or even 10,000x less data.
We used to build complex [big data systems][dds] *for ML*, just to train models that we thought might give
us a leg up. But now all that's out the door. Instead of spending money building data pipelines to squeak 
a bit more performance out of a model, you can instead spend the same money and solve 10x or 100x **more 
ML problems**. 

What business wouldn't want that?

The performance of these LLM-based models isn't as good as traditional ML models. They're also very 
expensive to run. So they're worse in most ways that ML algorithms were traditionally measured, but wildly
better in ways we hadn't thought of before. [Classic disruption][disrupt]. It's no wonder there's such
turbulent messaging about whether they're good or bad.


# An Example
_(it's fine to skip this section)_

Let's build a classifier model using an LLM. It's a program that tells us if a text is a spam message (yes/no). 
The cool part is that the first version involves no code at all,
and the amount of knowledge of data science methods increases fairly slowly as we progress through versions
of this.

## v1: No Code
Here's a contrived example for how to build one of these. Here's an LLM prompt:

```
You are given the task to classify text as 'spam' or 'not spam'. 
Here are some examples of spam.

TEXT: Win a free iPhone now!
ANSWER: spam

TEXT: Congratulations, you've won $1000!
ANSWER: spam

TEXT: Hi, how are you?
ANSWER: not spam

TEXT: Meeting at 3 PM in the conference room.
ANSWER: not spam

TEXT: Don't forget to send the report by Friday.
ANSWER: not spam


Now, classify the following text as 'spam' or 'not spam':

TEXT: {email_text}
ANSWER: 
```


You can drop this text into ChatGPT, or whatever your favorite tool is, and see how well it works. You
don't need to write any code at all to hash out the highest level details and measure performance. You might
even find that it performs best with no training examples at all (is it still machine learning if it doesn't
need data to learn?)


## v2: Embeddings
The problem with v1 is the LLM sometimes misunderstands the task, or misunderstands the output format (e.g.
explains why it's not spam instead of just writing "not spam"). Let's try again, but this time we'll use
embeddings. Embeddings are closer to traditional ML, but
they still use a large transformer model, so they carry a lot of the same benefits of LLMs.

An embedding model converts text into a list of numbers, called an embedding. You can think an embedding 
like coordinates (e.g. GPS) but for 1,500+ dimensions instead of 2. If you remember the equation from high 
school, `x^2 + y^2 = z^2`, you can use that same equation to find the difference between two texts. However, 
we typically use cosine similarity or dot product, but the principle is the same.


Use OpenAI to get the embedding:

```python
import openai
client = openai.OpenAI()

def get_embedding(text: str, model="text-embedding-3-small") -> list[float]:
    return client.embeddings.create(
        input=[text], 
	model=model,
    ).data[0].embedding
```

Use mostly unconfigured K-Means clustering:



```python
import sklearn

def train_model(training_data: list[str]) -> sklearn.clustering.KMeans:
    embeddings = [get_embedding(txt) for txt in training_data]
    model = sklearn.clustering.KMeans(k=2)
    model.fit(embeddings)
    return model
```


And then to use it:

```python
def is_spam(text: str) -> bool:
    embedding = get_embedding(txt)
    cluster_index = model.predict(embedding)
    return cluster_index == 0
```

This approach is a bit more code, still not much, but a lot faster and cheaper than LLMs while also maintaining the same
data efficiency benefits — you really only need 2-10 examples of a spam message to make this work. 

Embeddings are neat because they blend the old and new worlds of new machine learning.


# Effect on Privacy
I hear a lot of people concerned that LLMs have a negative impact on privacy. I'd argue the opposite — that the
massively improved data efficiency of LLMs and embedding models mean that it's much **easier to maintain
privacy**.

I say this after having worked with traditional ML algorithms for years. To make them work, we'd have to 
build training datasets that were big enough to train an accurate model. You can't typically get 10,000 records
from a single user, so we _**mix data from the entire user base**_ together.

Consequentially, a lot of security and privacy issues emerge.

If data goes into the model, it can also come out. If someone steals the model, they steal
private information from the entire training dataset. In some cases, they don't even need to 
steal the model, they can do it through an official production app interface.

With LLMs, the corporation responsible feels no urge to mix user data, because they can often get fine performance
without training on historical data. LLMs are cool, yo.


# Effect on Cost
I've worked for a lot of companies, and I know one thing to be universally true — they suck. They just suck
in different ways. It doesn't matter if you're at a FAANG or a hospital IT shop, it's not all roses.

The vast majority of companies struggle to build the data pipelines required for building ML training datasets,
so they make inefficient use of tools:

* Docker (here's my 2 GB image that I build several times per day)
* Kubernetes (🤦‍♂️)
* Spark / Databricks
* Over-scaled DynamoDB tables
* Expensive storage (e.g. using SQL instead of S3)

Sure all these problems are fixable on a company-per-company basis. But have you ever tried to fix this stuff?
It takes months, and that's only if you've already hired the right people, and even then they often make the problem
even worse, just in cooler ways. I've come to the conclusion that the
only way to fix the problem is to take the problem off the table entirely.

Remove the need for data hungry systems.

It's easy to spend **$10k per month** on a data pipeline, in a staging or test environment, _**that doesn't
serve any users**_. And since companies tend to scale for worst-case only, those costs spike upwards pretty fast when
you look at production.

Whereas LLM costs tend to scale proportionally to traffic, if you're using a provider like OpenAI or 
Azure OpenAI. If you get to the point where you're serving 10K requests per hour, the LLM costs are going
to be through the roof — but you've also proven that the use case is worth investing in, so you probably also
have budget to spend on engineers and data scientists to make it operate more efficiently.

LLMs & embedding models offer a way out.


# Conclusion
Whenever I hear someone say that they can't think of any uses for LLMs, I assume they don't have any experience
with traditional machine learning. Because if you've seen how all that works, all the wasted compute cost, all
the insecure "big data" systems, it's really hard to see nothing valuable in LLMs.




 [PRIMO]: https://ui.adsabs.harvard.edu/abs/2023ApJ...943..144M/abstract
 [boykis]: https://vickiboykis.com/2024/01/15/whats-new-with-ml-in-production/
 [compress]: https://pub.towardsai.net/stable-diffusion-based-image-compresssion-6f1f0a399202
 [dds]: https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/
 [disrupt]: https://www.hbs.edu/faculty/Pages/item.aspx?num=46
 [eht]: https://www.science.org/content/article/images-black-hole-reveal-how-cosmic-beasts-change-over-time
 [svm]: https://arxiv.org/abs/2308.16898
