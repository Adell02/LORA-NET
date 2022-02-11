<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Adell02/LORA-NET">
    <img src="img/logo.png" alt="Logo" >
  </a>

<p align="center">
    A unique radio network
    <br /><br />
    <a href="https://github.com/Adell02/LORA-NET/issues">Report Bug</a>
    ·
    <a href="https://github.com/Adell02/LORA-NET/issues">Request Feature</a>
  </p>
</div>

<p align="center"><strong>IMPORTANT! The project is being developed, for that reason, the features that aren't available at the moment will be marked as 🔴</strong></p>
<br />

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#user-nodes">User Nodes</a></li>
        <li><a href="#middle-nodes">Middle Nodes</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#hardware-connections">Hardware Connections</a></li>
        <li><a href="#files">Files</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a>
    <ul>
        <li><a href="#setup">Setup</a></li>
        <li><a href="#gui">GUI</a></li>
      <li><a href="#errors">Errors</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project
The aim of LORA net is to learn building a network based in 2.4GHz LoRa communication modules and ATmega328P U (Arduino Uno) as microcontroller. 

LORA net consists in a mesh network based in two kind of nodes: `User Nodes` and `Middle Nodes`. 

### User Nodes

Each user with an apropiate LoRa module and settings can access the network using the python-based desktop application in the <a href="https://github.com/Adell02/LORA-NET/GUI_v.0">GUI folder</a>. 
There are (to date) three main functions available for User Nodes:
<ul>
  <br />
  <li><strong>🔴Google Search:</strong> The node request to any other in the network with internet connection available a Google Search. The User receives the entries relative to that search and can choose from which of all to get the text in it. </li>
  <li><strong>Private Message:</strong> The desired message is sent to a specific node in the network (acording to an ID) if it's available.</li>
  <li><strong>File Transfer:</strong> Sending compressed via radio to any other user in the net</li>
</ul>

<p align="right">(<a href="#top">back to top</a>)</p>


### 🔴Middle Nodes

Most of the nodes of the network may be Middle Nodes in order to ensure a good performance of the net at long distances. These nodes are responsible for receiving, analyzing where are the packets addressed to and sending them again following the most efficient route when a transmission can't directly reach the recipient node.  


We are working to bring a feature that allows converting a User Node into a Middle Node whenever needed, imporving the net performance.

<p align="right">(<a href="#top">back to top</a>)</p>


## Getting Started
This project is based on the Arduino Uno and Semtech's modules SX127x. 

### Hardware Connections
<div>
  <img src="https://user-images.githubusercontent.com/84263340/153633151-c42c3546-dbfb-435a-bd68-98cd23723e13.png" width="200" height="200">
  <img src="https://user-images.githubusercontent.com/84263340/153633898-49054876-de93-42f7-8cde-cd6fd96ee445.png" width="200" height="200">
</div>

| SX127x  | Arduino Uno |
| ------------- | ------------- |
| NSS  | D10  |
| MOSI  | D11  |
| MISO  | D12  |
| SCK  | D13  |
| GND  | GND  |
| 3.3V  | 3.3V  |
| RST  | D9  |
| DIO0  | D2  |


<br />
<p align="right">(<a href="#top">back to top</a>)</p>


### Files
Every file regarding the uC is programmed with the Arduino IDE (C++). The main Arduino file (Arduino_GUI.ino) is located <a href="https://github.com/Adell02/LORA-NET/GUI_v.0/Arduino_GUI">here</a> and works in line with the main python program named <a href="https://github.com/Adell02/LORA-NET/GUI_v.0/">gui.py</a>.

Commenting our code is relevant to make it readable. 

(A more detailed explanation of each file will be written in the near future)

<p align="right">(<a href="#top">back to top</a>)</p>


## Usage
### Setup
The following steps indicate the procedure to SETUP the program:
1) `Download` or `clone the repository`
2) Connect the LoRa module to the Arduino Uno as shown <a href="#hardware-connections">here</a>.
3) Compile and upload the `Arduino_gui.ino` file located in directory `GUI_V.0\Arduino_GUI` 
4) Connect the `Arduino Board to your PC` via Serial (USB) and check which `PORT` is using (it may be "/dev/ACMx" in Linux and "COMx" in Windows).
5) Run `gui.py` located in directory `GUI_v.0`
6) On the top-right corner, write the `PORT` in use.

If there is a success message and no errors are displayed in the console, your user node is configured correctly.

In <a href="#errors">Errors section</a> you may find how to solve any error printed to the console. 

<p align="right">(<a href="#top">back to top</a>)</p>


### GUI
The interface consists on a small window built with `Tkinter` and is intended to be a simple but useful and interactive GUI. 

<div align="center">
<img src="https://user-images.githubusercontent.com/84263340/153661704-ac2f8225-d1c3-42b7-bd6c-7d41504fd93d.png" width="400" height="400">

</div>


It has a menu-bar with some options available such as Save (the console log), Exit (the program), Clear (the prompt) or Select All. 

On the right side of the window, there are some indicators whether the Node is `Sending` or `Receiving` a message/file/Google search from another one and also the `Port Configuration`.

A the center of the screen there are the fucntions available for User Nodes. Simply `fill the textbox and click the button next to it` to perform an action.

Underneath it, there is the `main console`. Here, all errors/ success messages are shown, as well as the information about the incomming and outcomming radio transmissions.

At the very bottom, there is a `loading bar` to indicate the transmission/reception duration.


<p align="right">(<a href="#top">back to top</a>)</p>

### Errors



<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

- [x] Build the main workframe (GUI and Arduino Basic transmission/reception)
- [ ] Add Google Search Functionality
- [ ] Improve Transmission Speed
- [ ] Ensure Communication with redundancy Checking
- [ ] Set ID's to each Node
- [ ] Manage simultaneous transmission without colliding
- [ ] Make Indirect communication through Middle Nodes
- [ ] Improve overall performance 

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch
3. Commit your Changes
4. Push to the Branch 
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

[Guillermo Adell](https://www.linkedin.com/in/guillermo-adell-vega-2409261b2/) - willyadell02@gmail.com

Project Link: [https://github.com/Adell02/LORA-NET](https://github.com/Adell02/LORA-NET)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

I'd like to add here some of the most helpful resources such as libraries, documents, GitHub repos...

* [Sandeep Mistry LoRa Library](https://github.com/sandeepmistry/arduino-LoRa)


<p align="right">(<a href="#top">back to top</a>)</p>

