---
layout: post
title: "FP For The Working Programmer: Why Is null Bad?"
categories:
 - fp-for-the-working-programmer
 - scala
---


Null is dangerous. This is a tough statement to accept for a lot of people I've worked with. The concept of null is deeply ingrained into the languages we use. In C/C++, if you access a member of a null pointer, the program can sometimes continue to run but generate strange results. This led to bugs that were sometimes very difficult to trace. Java improved the situation by causing programs to fail the instant a null pointer was accessed. 

Failing sooner rather than later makes bugs easier to trace, for sure. What if we could make the compiler disallow nulls?

{% highlight java %}
public class Foo {
	private String name = null;
	
	public int length() {
		return name.length();
	}
	
	public void setName(String name) {
		this.name = name;
	}
}

Foo foo = new Foo();
foo.length(); // KAPOW!!!
{% endhighlight %}

There are two kinds of values, (1) the ones that are there and (2) the ones that might not be. The trouble with the type systems of Java/C#/.../Ruby is that you can't tell the difference between these types. The null value is implicitly always available, so you have to always check for it even though it may not even make sense. 

Newer languages like Scala offer an Option type that represents something that can have no value. Here's the example in Scala:

{% highlight scala %}
class Foo {
  var name: Option[String] = None
  
  def length = name.getOrElse("").length
  def getName = name
  def setName(value: Option[String]) {
    name = value
  }
}

val foo = new Foo()
println(foo.length) // 0
foo.setName(Some("fred"))
println(foo.length) // 4
{% endhighlight %}

The `Option` type wraps a value; `Some("fred")` is non-null and `None` a lot like null. You can't access the value inside the option directly - `name.length` would result in a compile error. This could get cumbersome so the Option type has methods to make them fun again.

* `getOrElse(other: T): T` - get the value inside the option, otherwise use a default value
* `filter(predicate: T => Boolean): Option[T]` - returns an `Option[T]` but may turn a Some into a None. 
* `map[U](function: T => U): Option[U]` - safely converts the inner value to something else
* `flatMap[U](function: T => Option[U]): Option[U]` - safely converts the inner value to another option

Once you get comfortable with Options, your start writing less code and with fewer bugs. At some point you'll find that, more often than not, **the types only get in the way of the mistakes**. We're starting to see Option-like concepts in [Java][1], [C#][2] and [C++][3]. We'll talk more about Options later, but for now I'll leave you with this gem:

{% highlight scala %}
def doLogin(user: String, password: String) = ???

// only attempt an actual login if both user and password are given
def login(user: Option[String], password: Option[String]) = {
  user.flatMap(u =>
    password.flatMap(pw => doLogin(u, pw)))
}
{% endhighlight %}


 [1]: http://docs.oracle.com/javase/8/docs/api/java/util/Optional.html
 [2]: http://blogs.msdn.com/b/jerrynixon/archive/2014/02/26/at-last-c-is-getting-sometimes-called-the-safe-navigation-operator.aspx
 [3]: http://en.cppreference.com/w/cpp/experimental/optional
 [4]: http://www.infoq.com/presentations/Null-References-The-Billion-Dollar-Mistake-Tony-Hoare
 [5]: https://www.youtube.com/watch?v=nB2sXuYSH7k