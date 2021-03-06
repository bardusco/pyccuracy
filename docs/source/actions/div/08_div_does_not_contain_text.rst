=============================================
I see "some" div does not contain "some text"
=============================================

Syntax
------
::

	I see "<div name>" div does not contain "<expected text>"

where:
	``<div name>`` - name or id for the desired div element
	
	``<expected text>`` - text that this action needs to assert on
	
Description
-----------
Asserts that the specified div's current text does not contain the expected text.

.. note::

   The specified name will be checked against both "name" and "id" values. Only if neither of those match, the element is deemed not available.
   
.. note::

   This is not an exact match comparison. This means that if the expected text is a sub-set of the current text, this action will fail (if the current text is "some large text" and the expected text is "large" the action fails).


Raises
------
Raises ActionFailedError if the div's text does not contain the expected text.
This Exception is captured by Pyccuracy to assert that the test failed.
	
Examples
--------
::

	...
	Then
		I see "divSomething" div does not contain "some text"
	
*Rest of the test ommitted for clarity*

Changelog
---------
.. versionadded:: 0.4
   Div Does Not Contain Text action.
