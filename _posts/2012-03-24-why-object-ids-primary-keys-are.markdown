---
layout: post
title: "Why Object IDs & Primary Keys Are Implementation Details"
date: 2012-03-24
comments: false
---


Recently [I wrote a post](http://blog.timkellogg.me/2012/03/abstract-data-layer-part-1-object-id.html) about a project that I was working on with an abstracted data layer concept that can work in the context of either relational or document data store. In retrospect I think I brushed too quickly over the details of why I think object identifiers (and primary keys) are a part of the implementation that should be hidden, when possible. To explain what I mean I'll use a surreal-world story.


The Situation
-----------------

You are the chief software engineer at a software company. One day your product manager comes to you with a list of ideas for a new product where users can post definitions to slang words, like a dictionary. He says people are going to love this new app because everyone has a different idea of what  words mean. After talking with him to establish ubiquitous language and identify nouns and verbs, you crank up some [coding music](https://twitter.com/#!/search/%23codingmusic) and hack out some model classes.

{% highlight csharp %}
public class Word {
  public int Id { get; set; }
  public string Name { get; set; }
  public IList<Definition> Definitions { get; private set; }
}

public class Definition {
  public int Id { get; set; }
  public int WordId { get; set; }
  public string Text { get; set; }
  public string Example { get; set; }
}
{% endhighlight %}

A weekend later you finish coding the app using Int32s (`int`) as the identity data type for most of your models because it's usually big enough and works well as a primary key. Honestly, you didn't really think about it because its what you always do.

After the launch your app quickly gains popularity with the user base doubling every day. Not only that, but as more definitions get posted, more people are attracted to the site and post their own word definitions. While reviewing the exponential data growth figures, your DBA decides that `Definition.Id` should be changed to an Int64 (`long`) to accommodate the rapidly multiplying postings.

Let's stop for a minute and review what the _business needs_ were. Your product manager wants an app where people can post words and definitions. Each word has many definitions. There's no talk in the business domain of tables and primary keys. But you included those concepts in the model anyway, because that's how you think about your data.

The DBA chose to make the ID into a larger number to accommodate a larger amount of data. So now to help optimize the database, you are forced to update all your _business logic_ to work nicely with the _data logic_.


Data Logic Was Meant to Live in the Database
-----------------

The trouble with tying data logic closely to business logic is that the database isn't part of your business plan. As your application grows you'll have to tweak your database to squeeze out performance - or even swap it out for [Cassandra](http://cassandra.apache.org/). Databases are good at data logic because they are declarative. You can usually tune performance without affecting how the data is worked with. When you place an index, it doesn't affect how you write a SELECT or UPDATE statement, just how fast it runs.

At the same time, databases are also very procedural things. When you put business logic in stored procedures you lose the benefits of object oriented programming. It also makes unit tests complicated, slow, and fragile (which is why most people don't unit test the database). In the end, it's best to let your database optimize how data is stored and retrieved and keep your domain models clean and focused on the business needs.


The Type of the Object ID Is an Implementation Detail
-----------------

Lets say you hire a new COO that lives in Silicon Valley and thinks the latest coolest technology is always the gateway to success. With the new growth he decides that you should rewrite the dictionary application to use [MongoDB](http://www.mongodb.org/display/DOCS/Introduction) because it's the only way your application can scale to meet the needs of the business. While evaluating Mongo you draw out what an example word and definitions might look like when stored as [BSON](http://bsonspec.org/):

{% highlight js %}
{
  "_id": "09823bcf7de88c",
  "name": "LOL",
  "definitions": [
    {
      "text": "Laugh Out Loud"
      "example": "I can't wait for the wedding. LOL"
    },
    {
      "text": "Lots Of Love",
      "example": "I don't have the heart to let my mom know that LOL doesn't actually mean Lots Of Love"
    }
  ]
}
{% endhighlight %}

In Mongo, [you usually would store the Definitions inline with the Word](http://www.mongodb.org/display/DOCS/Schema+Design#SchemaDesign-EmbeddingandLinking). Now there is no need for a Definition.Id or Definition.WordId because all of this is implicit. Not only that, but Word.Id is now an [ObjectId](http://www.mongodb.org/display/DOCS/Object+IDs) - a very different 12 byte number that includes time and sequence components. In order to update your application to work with Mongo, you'll have to update all references IDs to use these ObjectIds.

The ID is an implementation concern. In a centralized SQL database, sequential integers make sense. In a distributed environment like Mongo, ObjectIDs offer more advantages. Either way, the type of your ID is an implementation detail.


Encapsulation Requires That You Hide Implementation Details
-----------------

Most OO programmers understand that encapsulation means that an object _has_ or _contains_ another object. However, some forget that a [large part of encapsulation](http://en.wikipedia.org/wiki/Encapsulation_(object-oriented_programming)) is that you should keep the [implementation details](http://stackoverflow.com/a/1777728/503826) of an object hidden from other objects. When the details of an object leak into other objects, the contract is broken and you [lose the benefits of the OO abstraction](http://www.joelonsoftware.com/articles/LeakyAbstractions.html).

Any ORM tool should give you the ability to select protected (if not private) members of the object to be persisted. If it doesn't, it's not using because it'll cause too great of a compromise in design. This is how we should have been allowed to write our objects from the start:

{% highlight csharp %}
public class Word {
  private object Id { get; set; }
  public string Name { get; set; }
  public IList<Definition> Definitions { get; private set; }
  public void Add(Definition definition) {
    if (definition == null) throw new ArgumentNullException();
    Definitions.Add(definition);
  }
}

public class Definition {
  public Definition(string text, string example) {
    Text = text;
    Example = example;
  }
  private object Id { get; set; }
  public string Text { get; private set; }
  public string Example { get; private set; }
}

{% endhighlight %}


But Dynamic Languages Diffuse The Problem
-----------------

If you're in a dynamic language like Ruby or Node.js this is less of an issue. Most of my argument hinges on the idea that your API will latch onto the object's ID and insist that all methods that use it will match. This is really just a constraint of strict statically typed languages. Even implicit typing will mitigate the issue some.

You can notice above that I got around the constraint by using `object` as the ID type. This is really what you want. It's telling the compiler and API that you really, shouldn't care what the type is - it's an implementation detail. You shouldn't run into many problems as long as you are keeping the ID properly encapsulated within the object.



