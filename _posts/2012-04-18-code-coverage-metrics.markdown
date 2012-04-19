---
title: Alternate Code Coverage Metrics
layout: post
categories:
 - engineering
 - code
---

Code coverage has been a controversial topic for a number of years. Just about everyone agrees that unit testing
is beneficial. The hardcore TDD folks push for 100% coverage, while everyone who's trying to make money has realized
that the last 1-5% can be very expensive code to test. So the conumdrum is knowing how much to test. How many tests
need to be written to get a high level of quality? I like a tweet from [Jimmy Bogard](https://twitter.com/#!/jbogard)

> In the "how much to test" argument, my line is when I **know** something works versus **hope** something works. 
> Hope is not a strategy.

As a developer, I think this is a great strategy. But when it comes to managing a company, it's very difficult to
know how much quality is degrading or improving over the past year when all you're measuring with is the strength of
a hunch. I really do think code coverage metrics have their place. But tying any kind of real incentives to any kind of code metrics is going to turn out to be a gigantic disaster.

The problem with code coverage is that, if you're not going for 100%, you're basically missing the point. Given a 
method:

{% highlight csharp %}
bool IsValid(string fileName)
{
  try
  {
    var stream = new FileStream(fileName)
    using (var reader = new StreamReader(stream))
    {
      var text = reader.ReadToEnd();
      var pattern = "<name>.*";
      pattern += text;
      pattern += ".*</name>";
      var pattern = new Regex(pattern);
      return !pattern.IsMatch(text);
    }
  }
  catch (FileNotFoundException)
  {
    return false;
  }
}
{% endhighlight %}

If you run a happy path test over this method, you get 89% coverage. Most people would consider this pretty decent
coverage for a whole project. However, you're still missing very important tests, such as when the file isn't found
or when the file either does or doesn't match the regex. Until you write those tests, your original happy path test
isn't really worth much and is really just providing a false sense of security.

Here, the hardcore TDD folks will point at the flaws in not insisting on 100% coverage. They're right, if you 
always followed the happy path and tested all your code like this, you'd have a reasonably high test coverage
with almost no faith in your tests.

I think an improved metric would be **percentage of classes with 100% coverage**. This acknowledges that some classes
shouldn't ever be tested, because they're too costly to test. But it also keeps with the spirit of 100% test
coverage. Combining this with a full code coverage percentage would lead to a *more* truthful number about quality
of tests. There's obviously still some holes in this method, but it's a lot closer.

