# HumanClassify Architectural draft

**Humaclassify** is intended to be a framework/blueprint for crowd-sourced classification of unknown objects.


The main purpose of the system is collaborative **classification**, in the sense of labelling an object with a category, but some other use cases could be implemented (multiple categories, voting, etc.).


The main use case is the following:

* an user (A) has some information about an object
* the user posts information on a shared place, where other users can access it
* users can add their own opinion about some features of the object
* the user A now has some more information about her "partially unknown" object.


A more concrete example:

* User (A) takes some pictures of a plant he cannot classify
* Other users can vote for the name of the plant by choosing from a predefined set of plants
* User A knows *what others think* about the plant name(s). Obviously this is not guaranteed to be the truth, but the information is supported by quotes and information about voters.


There might be some different models for this process, for example:

* The set of voters can be restricted
* The opinion of a voter can be editable or not by the voter herself
* The inquiry process could be closed at some point or left open (possibly changing in time)
* The requesting user could, at some point, "freeze" some attributes with values coming from the inquiry process (in an arbitrary/subjective way!)



## Terms

* **opinionated object**: is the main object the user wants to know about.
* **requesting user**: the user posting the opinionated object
* **judges**: the set of users that are allowed to add an opinion about an object
* **known features**: the attributes of the object that are considered to be true. (the requesting user has no doubt about them and they can be used as a for judges opinions)
* **opinionated features**: the attributes of the opinionated object unknown to the requesting user.


In general, an object attributes can be seen and classified from a broad range of perspectives, but we are mainly interested in the following:

* **data type**: the type of the attribute (string, integer, etc). Handled types may vary with respect of the backend storage system.
* **values domain**:
  * **Free**: can be set to any value compatible with data type (ex an integer)
  * **Set based**: allowed values are limited to a discrete set. (ex an integer in 1,2,3)
