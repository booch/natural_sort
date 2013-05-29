natural_sort
============

Python module for sorting lists naturally (i.e. 1.10 comes after 1.2).

This can be used to sort IP addresses, version numbers, variable-length alphanumeric product numbers, etc.
The lists to be sorted can contain strings, dictionaries, or objects.
For dictionaries and objects, the fields to sort on can be specified.

There's a good write-up on natural sorting at [Coding Horror](http://www.codinghorror.com/blog/2007/12/sorting-for-humans-natural-sort-order.html).


History
=======

I was writing an app for work, and thought it would be nice to have a natural sort for some of the tables (mostly for version numbers).
I couldn't justify writing it for work, but I thought the problem was interesting enough that I ended up writing it after hours.
Plus, I wanted to get some more experience with Python, as I had not used it for several years.


TODO
====

 * Use [hamcrest](https://github.com/hamcrest/PyHamcrest) for assertions.


Copyright / License
===================

Copyright 2013 by Craig Buchek

This code is released under the MIT license (other terms may be negotiated, if necessary):

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
