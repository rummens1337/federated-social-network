# Federated Social Network

Team F will develop the federated social network in this repository.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.
Instructions are made for Linux, but should also work for MacOS.

### Prerequisites

What things you need to install the software and how to install them

```
sudo apt install git make docker.io docker-compose
```
Make sure you are using Ubuntu 18.04 or higher to get the newest version of docker-compose.

### Installing
> Note: This guide assumes you are using ubuntu. The steps for Windows and MacOS are similar but not the same.
- Clone the git repository.
- Go into the cloned directory `cd team-f/`
- Copy (do not rename) the `config-dist.py` to `config.py` and configure the file.
- Run `make run` 
- In case make run fails, try to remove your docker containers and volumes using `make rm` and `make rm-images` 

### Default settings
- Central server, website on port 5000. Mysql on port 6000. Phpmyadmin port 7000.
- Data server, website on port 9000. Mysql on port 6001. Phpmyadmin port 7001.

## Optional arguments
```
make run type=data
make run port=XXXX
```

## Deployment

Production:

```
make run
```

Development:
```
make run debug=1
```

## Built With
```
?

<!--* [Maven](https://maven.apache.org/) - Dependency Management-->
<!--* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds-->
<!--* [Flask](https://palletsprojects.com/p/flask/) - Used for web-based application framework-->
<!--* [MySQL](https://www.mysql.com/) - Database management-->
<!--* []() - -->
```
## Contributing

...

## Versioning

<!--We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). -->
...

## Authors

* Danny#4659 Danny Opdam @10786708
* BasvdBrink#0409 Bas van den Brink @11322195
* Nick Moone#6119 Nick Moone @12488917
* coen_#3875 Coen Nusse @11902671
* Maqs#9499 Maqsood Ehsan @11219513
* iDylanK#2368 Dylan Kieft @11013575
* auke#7657 Auke Schuringa @11023465
* flix123#5242 Felix Hoekstra @11330600
* rummens#3150 Michel Rummens @13108093
* robop#7467 Tim Laamers @11320850

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

