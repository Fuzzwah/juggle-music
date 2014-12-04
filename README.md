Juggle Music
============

Juggle to trigger playback of samples. 

Uses OpenCV to track objects and Mingus to play midi samples based on object positions.

Very early stages of development.

My end goal is to have a system which flows along the lines of:

  * launch app
  * click each object to bind the tracker
  * trigger recording of a loop
  * juggle a pattern which lays down a drum loop
  * trigger stop record of loop
  * drum loop continues to play
  * juggling now triggers notes and samples to "play" the melody

My initial thinking is that the loop controls may need to be via a foot toggle, to free up the juggling to just trigger notes and samples. I can see that trying to use juggle tracking as the control method as well as the input method will be too complex.
