---
title: "Trappings: An easier way to do functional testing"
layout: post
categories:
 - unit testing
 - databases
 - open source
---

I've spent the last couple weeks piecing together a testing utility to fill a need. The problem is that we
need to run functional and integration tests that hit the database, but it's actually quite difficult. 
There's a few techniques that are traditionally used for setting up test data for automated tests. 

One possible solution is you can setup a script that populates the database before all tests run. But this
has the pesky problem of causing interdependent tests. One test might update an object that another test
makes assertions about, and suddenly you have false test failures that you have to spend time to debug.

Our case was even worse -- we were using our API to setup test data. Use the API to insert a user at the
beginning of the test and delete it at the end. When the `User INSERT` or `User DELETE` operations went 
haywire we got a whole ton of false test failures. You really should only test one thing with a test, and
our tests were getting way out of control.

The craziness drove me to write Trappings. Trappings provides a clear place for you to create test data
for .NET projects and have it torn down at the end of the test. It makes it possible to trivially write
functional tests that are independent of each other -- failures of one don't cause failures of another.

How to setup data
-----------------

Test fixtures are a place to declare data to be setup. Here is the sample from the readme:

{% highlight csharp %}
class TheRaceTrack : ITestFixtureData
{
  // A convenient pattern to follow is to make static properties for things
  // you'll access within the test. All of these are completely valid within
  // the using block.
  public static Car Cruze { get; set; }

  public IEnumerable<SetupObject> Setup() 
  {
    // Assign to static field for easy access later
    Cruze = new Car { Make = "Chevy", Model = "Cruze" };

    // cruze will be inserted into the database after this line
    yield return new SetupObject { CollectionName = "cars", Value = Cruze };

    // Since `cruze` has already been inserted, it's ID is already auto-assigned
    var tim = new Driver { Name = "Tim", CarId = Cruze.Id };
    yield return new SetupObject("drivers", tim);
  }
}
{% endhighlight %}

All you have to do is implement `ITestFixtureData` and not hide the default constructor. `Setup` returns
an `IEnumerable` which you can really use to your advantage. As each object is yielded, the next one isn't
constructed until the previous one is fully inserted into the database. This means you can take advantage
of MongoDB's ID auto-generation to piece together complex relationships.

Another feature is that classes can be public, private, nested -- whatever you need. If you want a 
fixture to be shared for a lot of tests, make it public. If you want more fixtures for specific use cases,
just toss them into nested classes and keep them close to the tests. The only constraints are placed by
the compiler. I find this can be very helpful.

A pattern I've begun following is to make static properties to hold references to objects I create during
`Setup()`. In the above example I can reference `TheRaceTrack.Cruze.Id` to get the ID of the Chevy Cruze.
For instance:

{% highlight csharp %}
[Test]
public void ILoveCars()
{
  using(FixtureSession.Create<TheRaceTrack>())
  {
    // Database is now setup. You can use code that assumes that documents
    // exist in db.cars and db.drivers

    var driver = from driver in drivers.AsQueryable()
                 where driver.CarId == TheRaceTrack.Cruze.Id
                 select driver;

    driver.Count().ShouldEqual(1);
  }
  // objects from TheRaceTrack are no longer accessible in Mongo
}
{% endhighlight %}

Here, we use the `FixtureSession` to create `TheRaceTrack` and ensure that the objects it creates will be gone
at the end of the `using` statement. Within the `using` statement we can do anything we want with these objects
-- including delete them. This works even for other processes, like a client-server architecture where you're 
testing the server from a client. Since the objects exist in the database, they exist globally (they're even 
accessible to other computers).

Disclaimers
-----------

While I haven't said it explicitly yet, this only currently works for MongoDB. I did it this way because that's
what I use most of the time and, frankly, it's stinkin easy. But there's no reason why this couldn't work for 
SQL or other databases, it's just not on my priority list. 

I've released the package on [NuGet][1] under the MIT license. My hope is that everyone can feel free to use it,
and contribute back if they find it useful.

 [1]: http://nuget.org/packages/Trappings
