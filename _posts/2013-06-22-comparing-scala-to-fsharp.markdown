---
title: An Unbiased Comparison of F# and Scala
layout: post
categories: 
 - fsharp
 - scala
 - functional-programming
---

Given my history as a .NET developer I learned Functional Programming via F#,
but I just started a new job as a Scala developer. Naturally, I've been 
comparing the two languages and the quirks and nuances that make could make
them enjoyable or problematic. To summarize quickly, I think Scala is more 
approachable but less "pure" than F#. Scala seems to have a diverse set of 
influences whereas F# tries to stick closely to proven Functional Programming 
basics.


Functional but Object Oriented
------------------------------

Both Scala and F# claim to be primarily functional languages but are also fully
object oriented. While F# is essentially OCaml.NET and Clojure is basically
Lisp for the JVM, Scala is a completely new invention. Scala also strikes
me as *more* object oriented than F#.

For instance, Scala includes both [mixins][2] and [monkey patching][3]. On
the other hand, F# only has monkey patching. Both concepts I learned from Ruby and 
I associate with pretentious arguments about "which is more OO". With that 
said, I love the fact that Scala has mixins. It's a much cleaner dependency
injection technique than IoC containers (which is how we did it in C#).  


Functions
---------

Given F#'s OCaml ancestory, it tends to define methods in an ML-like way. For 
example, an `add` function in F#:

{% highlight fsharp %}
let add a b = a + b
{% endhighlight %}

In the spirit of OCaml, this has a signature that looks something like 

{% highlight fsharp %}
int -> int -> int
{% endhighlight %}

which means, "a function that takes `int` and returns a function that takes
an `int` and returns an `int`". This plays perfectly into function currying and
partial function application where you might apply one argument at a time:

{% highlight fsharp %}
// add1 has type of int -> int
let add1 = add 3

// result is 7
let result = add1 4
{% endhighlight %}

Scala also has currying & partial function application, but it's less structured.
While F# functions are curried by default and ready for partial function 
application, Scala functions aren't but can easily be curried on demand:

{% highlight scala %}
def add(a: Int, b: Int) = a + b
val add1 = add(_, 3)
val result = add1(4)
{% endhighlight %}

Most of the time you don't *need* function currying, so I like that Scala makes
functions more familiar. But at the same time, currying isn't hard in Scala, 
since there's a native syntax for applying only some arguments via a pick-n-choose
templating style.


F# Is Stricter FP
-----------------

F#'s ML-style of function definitions that are curried by default makes for a 
more pure functional style. In F#, partial function application is used everywhere, 
so when doing `List` operations these functions are implemented in separate 
modules and "pipelined" using the `|>` operator:

{% highlight fsharp %}
[2; 3; 5; 8] |> List.map (fun x -> x * x) |> List.filter (fun x -> x % 2 == 0)
{% endhighlight %}

Result:

{% highlight fsharp %}
[4; 64]
{% endhighlight %}

On the other hand, Scala implements these methods as traits that are "mixed into"
`List`. Here's the same example in Scala:

{% highlight scala %}
List(2, 3, 5, 8).map(x => x * x).filter(x => x % 2 == 0)
{% endhighlight %}

I like to say that this means F# is more "pure" functional programming. 
I say this mainly because Scala chooses to use methods instead of plain functions in
cases like this. I'm not sure if this actually makes F# "better", but it is 
notable.


Discriminated Unions vs. Case Classes
-------------------------------------

This is a very powerful concept in both languages. You can't say you've mastered
either language until you've learned how to use them effectively. However, they're not
equal concepts.  Here's a quick overview:

{% highlight fsharp %}
type DimmerValue =
| On
| Off
| Dim of int

let value = Dim(50)
match value with
| On -> printf "it's on!"
| Off -> printf "it's off!"
| Dim(v) -> printf "romantically lit at %i" v
{% endhighlight %}

And the equivalent Scala code: 

{% highlight scala %}
sealed abstract class DimmerValue
case class On() extends DimmerValue
case class Off() extends DimmerValue
case class Dim(value: Int) extends DimmerValue

val value = Dim(50)
value match {
  case On => printf("it's on!")
  case Off => printf("it's off!")
  case Dim(v) => printf(s"romantically lit at $v")
}
{% endhighlight %}

The first point to contrast is that scala case classes are just a class hierarchy, 
whereas F# unions appear more like C enums but with different "shape". In reality,
F# unions are actually implemented as a class hierarchy, like Scala. 

In F#, all known values of the union must be declared in one place. However, Scala's 
class hierarchy approach means that you could define more values in other files or
JARs. This is the default behavior, but I included the `sealed` keyword which limits
definitions to the same file.

This seems like a bad default behavior to have. If the compiler doesn't know all 
possible values of a union, how can it determine correctness in a `match` statement?
There's definitely some loss of type safety there, but it is only a default, so 
I shouldn't complain too much.

Beyond that issue, there is F#'s concept of record types. They're immutable
classes that can't be inherited and have special semantics for copying:

{% highlight fsharp %}
type Person = { name: string; age: int, ssn: string }
let person = { name = "Tim"; age = 28; ssn = "123-45-6789" }
let olderPerson = { person with age = 31 }
{% endhighlight %}

Scala doesn't seem to have a record type concept. Instead, case classes are reused
for the same purpose. All case classes automatically get a `copy` method mixed in:

{% highlight scala %}
case class Person(name: String, age: Int, ssn: String)
val person = Person("Tim", 28, "123-45-6789")
val oderPerson = person.copy(age => 31)
{% endhighlight %}

I'm still undecided on whether I like how Scala merges the concepts. On one level,
it's simpler since there appears to be less concepts to learn. But on another
level, the semantics are broken - if you want a record type you have to define a
"case class" which infers that you'd normally use it like an enum.


Conclusion
----------

Scala is a more approachable language than F# but F# has a stronger
sense of type safety. F# also has a much stronger type inference system, which leads to
less type annotations. Regardless, I think Scala will recieve a much broader uptake
given that it has a much more familiar syntax to C/C++/Java/C# developers. On some 
level, I like to think of Scala as being more of "a better C#" than "like F#". Each
will have it's uses, but I think Scala will go far because of that.


 [2]: http://www.scala-lang.org/node/117
 [3]: http://jamesgolick.com/2010/2/8/monkey-patching-single-responsibility-principle-and-scala-implicits.html
