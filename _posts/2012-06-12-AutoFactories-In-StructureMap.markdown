---
title: How to use AutoFactories in StructureMap
layout: post
categories:
 - IoC
 - StructureMap
 - code
---

While watching the [StructureMap discussion on google groups][1], a user wanted to do AutoFactories in
StructureMap, something they were able to do in Castle.Windsor. I didn't
know what they were so I had to look through the code plus documentation of the Castle.Windsor feature. It turns
out that an AutoFactory is basically a specialized service locator that has no direct dependency on any kind
of container.  You write an interface that has methods to get instances from the container - but you let
StructureMap generate the implementation of this interface. Sound funny? Let me show you...

Example: A Plugin Framework
---------------------------

The first time I needed an AutoFactory was when I needed to create a plugin framework. The idea is that, if 
you want to execute some code on a specific event, you create a class that implements `IPlugin` and register
several implementations with the IoC container:

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
`container.GetAllInstances<IPlugin>()`.

The main problem we were running into is that we wanted to use `UserRepository` from a plugin, but we
also wanted to execute plugins from within a `UserRepository`. This introduces  an interesting dependancy
chain because (1) the controller requires (2) a plugin which requires (3) a repository which in turn
requires (1) a controller.

This is a circular dependency. StructureMap can't instantiate that graph bcause it can't create a controller 
without a controller already having been created (chicken and egg problem). StructureMap allows you to solve
this problem through property injection. This means that you create a constructor with less dependancies than
the class requires (a controller without a list of plugins or a plugin without a repository) and fill this 
dependency after instantiation via setting a property. I don't like property injection because
it's really just a bandaid over the real problem - you really shouldn't ever need circular dependencies.

In our case we were able to use an AutoFactory:

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
plugins - you don't have to inform them how your application is structured, only what the interfaces are.
Second, you also decouple the lifespan of each plugin object from the lifespan of the `PluginController`.

It's a Service Locator, But Not An Anti-Pattern
-----------------------------------------------

Now, you may be cringing at the idea that I might be advocating the use of the [service locator][2] 
[anti-pattern][3]. Or at least you should be! Sevice locators should be avoided because they hide 
dependencies (especially if you use a static service locator instead of building the whole object
graph). Also, having a hard dependency on the IoC container couples your application to the container --
kind of ruins the point of using IoC in the first place.

Most of the time when we're using the IoC pattern we try to create the whole object graph all at once
because it clearly shows dependencies. Sometimes, as in the plugin example, we need to break off part
of the object graph and create it separately. There are lots of legitimate reasons to do this, plugins
are only one. When you run into a situation like this, the AutoFactory makes it possible and clean.

Martin Fowler actually [encourages the usage of service locators][5] but warns that they can be implemented
badly. His main concern is that the implementation isn't decoupled from the usage with an interface (I've
seen static service locators cause huge problems). Honestly, I think the AutoFactory is a great example
of a legitimate use of a service locator pattern. Maybe it's not really an anti-pattern after all...

 [1]: https://groups.google.com/forum/?fromgroups#!forum/structuremap-users
 [2]: http://commonservicelocator.codeplex.com/
 [3]: http://blog.ploeh.dk/2010/02/03/ServiceLocatorIsAnAntiPattern.aspx
 [4]: http://kozmic.pl/dynamic-proxy-tutorial/
 [5]: http://martinfowler.com/articles/injection.html#UsingAServiceLocator 
