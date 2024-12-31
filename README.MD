[![SphereOnCircle Animation Thumbnail](thumbnail.jpg)](https://github.com/youroldmangaming/3D-SineWave-Animation/blob/main/SphereOnCircle.mp4)

Or watch it on [YouTube](https://youtu.be/wXhSkg9iTU8).

Run Code

manimgl sphere_on_circle.py SphereOnCircle 


Create Video
manimgl -w --uhd sphere_on_circle.py SphereOnCircle

or

ffmpeg -i SphereOnCircle.mp4 -vf "fps=60,scale=640:-1:flags=lanczos" -c:v pam -f image2pipe - | convert -delay 5 -loop 0 - sphere_animation.gif


