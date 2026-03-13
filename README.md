# CS50 Games in Python

[CS50 Games](https://cs50.harvard.edu/games/)

## Lessons

### Delta Time

Delta time (dt) is the time it took the computer to render the last frame.

A fast computer will process the frame much more quickly than a slow computer.

Capping framerate does not solve this problem. If you cap the speed limit so that sports cars are limited to 60mph, it doesn't speed up a horse and cart travelling at 10mph.

`clock.tick(60)`

Delta time allows movement to be measured against time, not framerate. As such, both slow and fast computers will show a sprite moving the same distance in the same time. The difference is that the fast computer will display more frames during that period, resulting in smoother movement.

`updated_pos += vector * speed * dt`

[Clear Code - Understanding framerate independence and deltatime](https://www.youtube.com/watch?v=rWtfClpWSb8&t=1557s)

### State Machines



## Problems

### Artefacts

Pixels are counted in whole numbers. You can't print half of a pixel to the screen.

## Readings

[How to Make an RPG](https://howtomakeanrpg.com/)
[Game Programming Patterns, by Robert Nystrom](http://gameprogrammingpatterns.com)
