In order to make this work as an exe, you have to edit appjar..

lines 500+

the check for if windows add icon, remove that.

comment it out, whatever. 

it will build after that.


BUILDING:

Use EITHER python 2.7x (will work unmodified)
or python 3.3/3.4 and UNDER (may dependencies will need to be adjusted, particularly tk)

pyinstaller -F -w renamer-gui.py