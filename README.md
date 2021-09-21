
Reference
---------

* [Learn Python by making a text-based adventure game](https://coding-grace-guide.readthedocs.io/en/latest/guide/lessonplans/beginners-python-text-based-adventure.html)
* [TEXT-BASED ADVENTURE GAME USING PYTHON](https://cppsecrets.com/users/5617971101051071011161151049711410997484852494964103109971051084699111109/Text-based-Adventure-Game-using-Python.php)
* [Making a Text Adventure Game with the cmd and textwrap Python Modules](https://inventwithpython.com/blog/2014/12/11/making-a-text-adventure-game-with-the-cmd-and-textwrap-python-modules/)
* [Colossal Cave Adventure](https://en.wikipedia.org/wiki/Colossal_Cave_Adventure)
* [13 Tips For Writing a Good Text Adventure Game](https://www.davidepesce.com/2020/02/26/13-tips-for-writing-a-good-text-adventure-game/)
* [Python Text Adventure Script](https://codingtoolsandresources.blogspot.com/2019/01/python-text-adventure-script.html)
* [Python text based game - Ideas?](https://www.daniweb.com/programming/software-development/threads/423125/python-text-based-game-ideas)
* [How to create a text-based adventure game in Python?](https://www.askpython.com/python/text-based-adventure-game)
* [trinket adventure](https://trinket.io/python/e5a03e7cbc)
* [Python-RPG](https://github.com/FlorianLeChat/Python-RPG)



example games
-------------

* [Portcullis](https://media.textadventures.co.uk/games/WqnTZlbAy0KTtqjoH5l-Lg/index.html)
* [Portcullis Help](https://media.textadventures.co.uk/games/WqnTZlbAy0KTtqjoH5l-Lg/porhelp.html)
* [Fogwick](https://playfic.com/games/JeneLandsquid/fogwick)
* [Blight of Elantria](http://play2.textadventures.co.uk/Play.aspx?id=oipb_nhu8esmxdrryqfz2a)
* [textadventures](https://textadventures.co.uk/games/tag/fantasy)
* [Dragon Story III](http://play2.textadventures.co.uk/Play.aspx?id=rrepqgh8w02htemhxyh5vq)
* [textgame](https://github.com/davekch/textgame/blob/master/example.py)
* [The Magic Circle](https://playfic.com/games/patcrosmun/the-magic-circle)

unrelated, but fun:

[Choice of Dragons](https://www.choiceofgames.com/dragon/)

schema
------

### places

* name
* description
* objects
* go
    * north
    * south
    * east
    * west
    * up/down
    * out/in

### inventory

* qty
* name

### items

* name
* desc
* for-sale
* price
* can-take

#### ideas

- satchel
- key
- scroll with magic words
- animal
- lyre
- mysterious box
- armour
- lamp / lantern
- bottle
- magic box - sword, wand, daggar
- Nach dem Spiel ist vor dem Spiel.

### actions

* enter
* take/drop
* say/ask
* move/open
* use/with

* go
* e[x]amine/search
* look

### character

* name
* type


design
------

locations

* home
    * door
    * bed
    * chest
* cave
    * dragon
    * treasure
* market
    * elixr
    * shield
    * cloak



Layout
------

```
  +--------------------+-------+------------------+-----------------------------------------------------------------+
  |         0          |  1    |       2          |               3                                                 | 
  |                                                                                                                 | 
  |                                                                                                                 | 
  |                          Town                                                                                   | 
  |                        ╔════════════════════════════════╗                                                       | 
  |                        ║    +----------+                ║                                                       | 
  |                        ║    |          |                ║                                                       | 
  |1                       ║    |  Market  |                ║    Forest                                            1| 
  |                        ║    |          |                ║                                                       | 
  |                        ║    +---+  +---+                ║                                                       | 
  |                        ║        |  |                    ║                                                       | 
  +-   +----====----+      ║        |  |                    ║                                                      -+ 
  |    | . ++++++++ |      ║        |  |                    ║                                                       | 
  |    | .          +------╬--------+  +--------------------╬----------------------------------+                    | 
  |0   | . home        Courtyard   Path                     ║    Road                          |                   0| 
  |    | .          +------╬--------------------------------╬-------------------------------+  |                    | 
  |    | . ______  O|      ║                                ║                               |  |                    | 
  +-   +------------+      ║                                ║                               |  |                   -+ 
  |                        ║                                ║                               |  |                    | 
  |                        ║                                ║                            +--+  +--+                 | 
  |                        ║                                ║                            |        |                 | 
  |                        ║                                ║                            |  Cave  |                 | 
  |-1                      ║                                ║                            |        |               -1| 
  |                        ║                                ║                            +--------+                 | 
  |                        ║                                ║                                                       | 
  |                        ╚════════════════════════════════╝                                                       | 
  |                                                                                                                 | 
  |        0          |  1    |       2          |               3                                                  |                                                                                                                 | 
  +-------------------+-------+------------------+------------------------------------------------------------------+                                                                                                                -+ 
                                                             
```
