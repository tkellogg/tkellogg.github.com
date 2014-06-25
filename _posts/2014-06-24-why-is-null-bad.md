---
layout: post
title: "FP For The Working Programmer: Why Is null Bad?"
categories:
 - fp-for-the-working-programmer
 - scala
---


Is null bad? Why is it bad? Is it bad enough for me to care? - These are all questions I remember asking. Hopefully I can quickly answer them for you.

If you reference variables that are null, they have a bad habit of making your programs crash. For instance check out this Java code:

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

The working programmer will be quick to point out "yeah, the dumbass programmer forgot to check for null". This is true, lets just go ahead and fix that.

{% highlight java %}
public class Foo {
	private String name = ""; // change #1
	
	public int length() {
		return name.length();
	}
	
	public void setName(String name) {
		// change #2
		this.name = (name == null ? "" : name);
	}
}
{% endhighlight %}

There are two kinds of values, (1) the ones that are there and (2) the ones that might not be. The trouble with the type systems of Java/C#/.../Ruby is that you can't tell the difference between these types. In the example, if `name` could be non-nullable string this program would be a lot simpler. This is how we would do it in Scala:

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

Once you get comfortable with Options, your start writing less code and with fewer bugs. At some point you'll find that, more often than not, the types only get in the way of making mistakes. We'll talk more about Options later, but for now I'll leave you with this gem:

{% highlight scala %}
def doLogin(user: String, password: String) = ???

// only attempt an actual login if both user and password are given
def login(user: Option[String], password: Option[String]) = {
  user.flatMap(u =>
    password.flatMap(pw => doLogin(u, pw)))
}
{% endhighlight %}


