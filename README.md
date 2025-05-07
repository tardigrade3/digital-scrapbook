# DigiScrap
A web app to build a scrapbook with your friends and family.

## Features

* From the home page, the user can create a new scrapbook project or enter a scrapbook code to access a preexisting project
* When creating a new scrapbook, the user chooses the title and theme.
* Each scrapbook project is assigned a 6-character code which the user can share with friends or family so they can add their own photos.
* From the scrapbook page, the user can upload images with captions and then generate a pdf with their uploaded media formatted as a scrapbook.
* The user can edit captions of images or delete them.
* The user can change the name and theme of their scrapbook project and delete their scrapbook.

## Installation

* Uses Django version 3.2 with Python 3.7.0
* ReportLab version 4.1
* SQLite 3 (this is included in Python)

See requirements.txt for the list of required packages.

The terminal command to run a local development server with Django is:
```
$ python manage.py runserver
```

## Known Bugs

* Some uploaded portrait images are displayed in landscape in the exported scrapbook pdf.
* Some images do not load when DEBUG is set to False in settings.py

## Support

Julia Kirney: jkirn1@ocdsb.ca

Irha Imtiaz: iimti1@ocdsb.ca

Maryum Dada: mdada1@ocdsb.ca

## Sources

###Sources used during development of code:

Caleb Curry. “How to Upload an Image Using Django ImageField (the RIGHT Way).” YouTube, 10 Mar. 2022, www.youtube.com/watch?v=fsVY66QBhwM. Accessed 12 Apr. 2024.

Codemy.com. “Style Django Forms with Bootstrap - Django Blog #5.” YouTube, 10 Apr. 2020, www.youtube.com/watch?v=6-XXvUENY_8&list=PLCC34OHNcOtr025c1kHSPrnP18YPB-NFi&index=6. Accessed 21 Mar. 2024.

Codemy.com. “Using Databases with Django - Django Databases #1.” YouTube, 3 Feb. 2020, www.youtube.com/watch?v=A1nqCgAM6CE. Accessed 6 Feb. 2024.

“Django Documentation.” Django Project, Django Software Foundation, docs.djangoproject.com/en/5.0/. Accessed various pages from the Django documentation website throughout development.

“Python and Django Tutorial in Visual Studio Code.” Visual Studio Code, Microsoft, code.visualstudio.com/docs/python/tutorial-django. Accessed 6 Feb. 2024.

“ReportLab PDF Library User Guide.” ReportLab, Wimbletech, www.reportlab.com/docs/reportlab-userguide.pdf. Accessed 17 Apr. 2024.

Websites such as Reddit and Stack Overflow were also used.

###Images:

collaborapix. “Pixel Art Illustration Scissors Pixelated Scissors Tools Scissors Cutter Pixelated,” Freepik, www.freepik.com/premium-vector/pixel-art-illustration-scissors-pixelated-scissors-tools-scissors-cutter-pixelated_80978371.htm. Accessed 12 Apr. 2024.

PINK AESTHETIC S. “Pink Heart Illustration Transparent Background PNG Clipart,” HiClipart, www.hiclipart.com/free-transparent-background-png-clipart-zucww. Accessed 19 May 2024.

All other images are from Canva.

###Fonts:

Boucherie, Thomas. “Daughter of Fortune Font.” Dafont.com, 7 Feb. 2022, www.dafont.com/daughter-of-fortune.font. Accessed 16 Apr. 2024.