![alt text](https://raw.githubusercontent.com/0verloader/Vping/master/Vping%20Logo.png)

# A peer to peer network for the masses 

An overlay network that can be based anywhere and accessed by anyone.
Main goal is to make an efficient, safe and fast network for sharing data with
people you share interests with. Give it a try!

## Getting Started

Just clone the project to your computer and run make, it's simple as that !

```
git clone https://Arakadakis_k@bitbucket.org/Arakadakis_k/networking.git
```

### Prerequisites

Most Linux distros and Mac OS come preinstalled with the python compiler
but if you find any trouble, these are the links to follow :

* python - https://www.python.org

In order to run trackR you will need :

* matplotlib ( apt-get install python-matplotlib )

* pyplot

* networkX ( https://github.com/networkx/networkx.git )


## Running

```
mkdir trackR
```
```
mkdir peer1
```
```
cp networking/peer/peer.py peer1
```
```
cp networking/trackR/* trackR
```
```
python trackR/trackR.py xxxx
```
```
python peer1/peer.py yyyy zzzz.zzzz.zzzz.zzzz xxxx (yyyy: peer port , zzzz.zzzz.zzzz.zzzz: trackR ip , xxxx: trackR port)
```


### Break down into end to end tests

When a trackR is live 'n' users can connect to the network (trackR) in order to send and download files.
Requests from peers (users) are handled by the trackR who controls the flow of the network.
Communication between peers is the key to speeding up sharing. 

1) Peer requests
```
download www.python.com
```

## Built With

* [python](https://www.python.org) - everything

## Contributing

~ Arakadakis Konstantinos
~ Tsiakkas Ioannis

## Versioning

I use [SemVer](http://semver.org/) for versioning. For the versions available. 

## Authors

* **Arakadakis Konstantinos** - *(konstantinosAR)* - [konstantinosAR](https://github.com/KonstantinosAR)
* **Tsiakkas Ioannis** - *(Keybraker)* - [Keybraker](https://github.com/keybraker)

## License

This project is licensed under the ITE-TNL License