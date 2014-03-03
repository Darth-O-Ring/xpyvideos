X-Py-Videos
-----------
-----------

X-Py-Videos is a program written in Python that allows for the downloading
of videos from the websites www.xvideos.com, www.xhamster.com, www.redtube.com, and www.youtube.com.

The Pytube library is now included by default in packages.

Options:

url(Positional Argument)

-f/--filename(Default: video title | video format's extension is added automatically -- youtube videos have format 
		options chosen at runtime)

-dir/--directory(Default: current working directory)

-c(Only for youtube videos) (Convert video to mp3 file)

-do(Only for youtube videos) (Delete original video file if -c is given)

Running setup:

cd xpyvideos/

sudo python2 setup.py install

Example usage:

xpyvideos http://www.xvideos.com/remaining_link -f xvideo_movie -dir xvideo_stash/

if using multiple links and filenames:

xpyvideos http:www.xvideos.com/remaining_link,http:www.youtube.com/video_id -f xvideo_movie,youtube_movie -dir video_stash
