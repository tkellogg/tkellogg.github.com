---
title: AutoFactories in StructureMap
layout: post
categories:
 - IoC
 - StructureMap
 - code
---

Recently I became heavily involved in the StructureMap project. I highly recommend any developer to try 
following a google groups mailing list of a open source project. I've done it for [Moq][1] in the past,
which is where I learned about all kinds of features, like how `Mock.Of<Author>(x => x.Name.First == "Tim")`
can rapidly shorten your mock setups. But this post isn't about Moq, It's about a feature I learned about
in StructureMap. Or, more specifically, it's about a feature that I learned about in Castle.Windsor that
is re-implemented in StructureMap.

A user wanted to do AutoFactories in StructureMap, something they were able to do in Castle.Windsor. I didn't
know what they were so I had to look through the code plus documentation of the Castle.Windsor feature. An
AutoFactory is basically a specialized service locator that has no direct dependency on any kind of container.
You write an interface that has methods to get instances from the container - but you let StructureMap generate
the implementation of this interface. 

Example: A Plugin Framework
---------------------------

The first time I needed an AutoFactory was when I needed to create a plugin framework. The idea is that, if 
you want to execute some code on an event, you create a class that implements `IPlugin` and register it with
the IoC container:

{% highlight csharp %}
public interface IPlugin
{
	void Execute();
}
{% endhighlight %}

_Note: I'm simplifying this quite a bit. The actual plugin framework has more complexity, but it esentially 
boils down to this._

We created a plugin controller to execute all plugins and handle failures. Our initial implementation
looked something like this:

{% highlight csharp %}
public class PluginController : IPluginController
{
	private readonly IList<IPlugin> plugins;

	public PluginController(IList<IPlugin> plugins) 
	{
		this.plugins = plugins;
	}

	public void Execute() 
	{
		foreach(var plugin in plugins) 
		{
			plugin.Execute();
		}
	}
}
{% endhighlight %}

When you take any sort of `IEnumerable` through the constructor, StructureMap (or any IoC container) will 
give you a list of all registered instances of that type. This is similar to when you call 
`container.GetAllInstances<IPlugin>()`. The main problem we were running into is that we wanted to use
`UserRepository` from a plugin, but we also wanted to execute plugins from within a `UserRepository`. 

The problem is that means we would have to introduce a circular dependency. Circular dependencies have a way
of breaking StructureMap without the usage of property injection. I also don't like property injection because
it's really just a bandaid over the real problem -- you really shouldn't ever need circular dependencies. In
our case we were able to use an AutoFactory.

{% highlight csharp %}
public interface IPluginFactory
{
	IList<IPlugin> GetPlugins();
}
{% endhighlight %}

We then register this interface like this:

{% highlight csharp %}
For<IPluginFactory>().CreateFactory();
{% endhighlight %}

There is no implementation of this interface. The `CreateFactory()` extension method means that StructureMap
will create a [dynamic proxy][4] object that has a one-liner implementation of `GetPlugins` that just returns
`ObjectFactory.GetAllInstances<IPlugin>()`. 

With this fancy new `IPluginFactory`, we change `PluginController` to use it:

{% highlight csharp %}
public class PluginController : IPluginController
{
	private readonly IPluginFactory pluginFactory;

	public PluginController(IPluginFactory pluginFactory) 
	{
		this.pluginFactory = pluginFactory;
	}

	public void Execute() 
	{
		foreach(var plugin in pluginFactory.GetPlugins()) 
		{
			plugin.Execute();
		}
	}
}
{% endhighlight %}

This new implementation isn't really any more complex, but it solves two problems. First, you no longer
have to think about circular dependencies. This is great if you're letting third parties develop these 
plugins -- you don't have to inform them how your application is structured, only what the interfaces are.
Second, you also decouple the lifespan of each plugin object from the lifespan of the `PluginController`.

It's a Service Locator, But Not An Anti-Pattern
-----------------------------------------------

Now, you may be cringing at the idea that I might be advocating the use of the [service locator][2] 
[anti-pattern][3]. Yes, we do have an object that directly accesses the container -- much like a service
locator pattern. However, I don't think this falls into the same pitfalls as the service locator. Most
criticisms of the service locator is that you have a _dependency injection_ framework but you have a 
dependency on the container, which kind of ruins the point. 

In the AutoFactory, none of your code actually references the container. If you were to switch to a simpler
IoC container that didn't support AutoFactories, you could still write your own implementation that received
a `IContainer`, but it isn't necessary unless you actually make the switch.

The AutoFactory, in my opinion, still relies on the same principles of inversion of control. Dependencies are
clearly labeled and we become agnostic about the implementation. Therefore, I highly recommend using an 
AutoFactory if you run into a situation where it's helpful.


 [1]: moq google groups
 [2]: service locator
 [3]: service locator anti-pattern
 [4]: dynamic proxy
