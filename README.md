trussvis
========

Web-based 2D truss design &amp; optimization environment

A web-based IDE for designing 2D trusses. Most activity is
mouse-driven; uses a 'mode' metaphor rather than a 'tool' metaphor.
Flask backend with D3/SVG frontend.

Allows the user to create a truss, specifying locations of joints and
members, also member material and thickness. The user can also apply
loads and constraints to any joint. In its current form, the program
performs a static analysis and colors each member to indicate stress
(relative to failure stress.)

Future versions will use a gradient descent algorithm to improve the
design by adjusting joint positions and edge thicknesses. More ambitious
future versions might make changes to the overall topology.

Live at http://trussvis.herokuapp.com
Code at http://www.github.com/nathanwbrei/trussvis


