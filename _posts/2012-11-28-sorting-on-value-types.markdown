---
layout: post
title: "Value Types and Memory Usage"
date: 2012-11-28
comments: false
categories:
 - code
 - csharp
---

Last week a respected colleague mentioned off hand that sorting on a value type takes a lot of memory in 
C#. Interested, I looked into this to see why/when this is true.
 
Value types (using the `struct` keyword) are always passed by value, unlike reference types (`class` 
keyword) which are always passed by reference. This means that every time you pass them into a method, the 
whole value is copied; whereas with reference types, only the reference (pointer) is copied. Pointers are 
4 to 8 bytes, so his original statement is only of concern if your value types are larger than that. 
Some such types are DateTime, Guid, and BsonObjectId.
 
Some people like to think of value types as being allocated on the stack (versus the heap). In C#, [this 
is irrelevant][1]. The CLR allocates value and reference types wherever it feels like. Usually, local variables
and parameters are stored on the stack (or registers) and values that are members of a class are usually
allocated on the heap. It was done this way because the folks who wrote the CLR believe they can do a
good enough job of optimizing stack and heap usage, so you shouldn’t worry about it. If you’re in C#, you
shouldn’t care where they’re allocated. If you’re doing something that requires you to care, you need to
either break into an [unsafe C# code block][2] or [C++][3].
 
As for his actual statement – yes, using Base Class Library algorithms for sorting on value types will
take more memory for value types than reference types because it has to copy values. However, there are
exceptions to this.
 
You can always write method parameters with the `ref` keyword so they’re passed by reference. This would
fix the problem of copying, but the all of the BCL classes[\*](#gen) are written generically by using `IComparable`
or some other interface. When you cast a value type like an `Int32` to an interface like `IComparable`, it
has to be boxed into a reference type. When boxing, the CLR allocates a managed reference type object
and then copies the `Int32` value into the managed container. It copies the value again when unboxing.
 
In summary, sorting on a value type can take quite a bit more memory than sorting on reference types.
However, it is possible to write your own sorting algorithm that always passes by reference and doesn’t
use any additional memory (but who does that?). 

### Notes

\* *One might point out that generic classes like `List<int>` have a [`Sort()`][4] method.  However, this casts `int` to `IComparable` while sorting.* 

 [1]: http://blogs.msdn.com/b/ericlippert/archive/2009/04/27/the-stack-is-an-implementation-detail.aspx
 [2]: http://msdn.microsoft.com/en-us/library/t2yzs44b.aspx
 [3]: http://msdn.microsoft.com/en-us/library/aa288468(v=vs.71).aspx
 [4]: http://msdn.microsoft.com/en-us/library/b0zbh7b6.aspx
