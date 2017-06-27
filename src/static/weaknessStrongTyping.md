# Weakness of Strong Typing

Overview: In a computer language like Java, the datatypes are declarative and lends itself to strict type checking at compile time and other types of error checking at run time. However such strict type checking makes programming laborious and long with a lot of boiler plate code. Stricting type checking leads unnecessary rules, which result in unnecessary frameworks, and makes programming more complex and inflexible that it needs to be. These pitfalls of Strict typing are examined here.

Narrative:
Strict type-checking has hidden pitfalls and one of the biggest one is the convoluted design and frameworks necessary to by-pass this strict typing! It is necessary to by-pass type checking for program brevity and comprehensibility.  Several examples of such framework/convoluted design issues are ingrained in Java. Some major ones are:

1. Templating functions/classes: This is a technique of not specifying the type and denoting it by '<T>' which stands for any type. Templating functions and classes have their own set of rules. This is a convoluted technique which is completely avoided by non strictly typed languages such as Python.

2. Dependency Injection: This is a technique of the 'framework' 'injecting' objects/properties into other classes. Again this is convoluted and has many rules regarding 'constructor based injection' and 'setter based injection'. Besides these it makes use of other artifacts (like interfaces). The idea is that the framework can pick an appropriate class to inject based on it being declared as implementing a specific interface. This entire complexity is avoided by non strictly typed languages such as Python.

3. Aspect oriented programming - a technique of injecting pieces of standard useful template code around a application code block to decorating it. This may be useful to record auditing information, checking for privileges and similar purposes. This again involves following the rules of the framework, which can be convoluted in a strictly typed system. Python for example solves this elegantly by the use of decorators, which are not only simple, but are intuitive and more functional than similar structures in Java.

4. Semantic vs Strict typing: Strict typing can on occasion be at odds with the meaning of the data. For example: we may decide that we need a function to return different types depending on the types in the input. In strict typing this is not possible. Non-strict typing is a solution to this problem.

5. Method overloading. Strict typing requires different methods, in case a method can take input of different types. Such overloading results to coding functions for each type. Non strict types (Python) completely avoid such convoluted coding.

6. Strict typing also necessitates well defined structures. This makes it impossible to add methods, properties dynamically to an object.

7. Dynamic data structures: Strict typing requires data structures to be explicitly declared. This requires multiple changes in the code and is much harder to keep track of as compared to the ease with which data structures can be manipulated in Python.
