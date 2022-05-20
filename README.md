# BachelorProject
My implementation of [Tutte embedding](https://en.wikipedia.org/wiki/Tutte_embedding) using OpenGL and Python

Jiří Povolný <urlikpov@gmail.com>

## How to use:
* Input abstract graph to [input_graph.txt](https://github.com/Urlikp/BachelorProject/blob/master/input_graph.txt), the graph should be planar and 3-connected:
  * Line 1: N (integer, number of nodes)
  * Line 2: A B (node A is connected with node B, A and B are integers)
  * ...
* Run in Ubuntu terminal:
```bash
$ sudo bash install_requirements_ubuntu.sh
$ bash build.sh
```
* build.sh options:
```bash
    -h  Print help and exit script
    -a  Generate starting random coordinates for all nodes
    -f <face>
        Choose custom main face, it should be in form: "node_1,node_2,...,node_n", for eample: "0,1,5,4"
```


## Videos:
[Playlist](https://www.youtube.com/playlist?list=PLBuG_2a4g9lFZwrufIdn3p1itkugLSZvh)

Click on image to play video:

[![Video](http://img.youtube.com/vi/SoTiWwz-qig/0.jpg)](https://youtu.be/SoTiWwz-qig)

## Screenshots:

![Screenshot_01](https://github.com/Urlikp/BachelorProject/blob/master/Media/graph_1.png)
![Screenshot_02](https://github.com/Urlikp/BachelorProject/blob/master/Media/graph_focus_1.png)
