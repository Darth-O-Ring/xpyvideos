X-Py-Videos:

X-Py-Videos is a program written in Python that allows for the downloading
of videos from the websites www.xvideos.com, www.xhamster.com, www.redtube.com, and www.youtube.com.

YouTube support depends on:

https://github.com/NFicano/pytube.git

Options:

url(Positional argument)

-f/--filename

-dir/--directory

-c(Only for youtube videos) (Convert video to mp3 file)

-do(Only for youtube videos) (Delete original video file if -c is given)

Running setup:

cd xpyvideos/

sudo python2 setup.py install

Example usage:

xpyvideos http://www.xvideos.com/remaining_link -f xvideo_movie -dir xvideo_stash/
