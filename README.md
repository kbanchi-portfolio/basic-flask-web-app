**Table of Contents**

- [basic-flask-web-app](#basic-flask-web-app)
  - [About The Project](#About-The-Project)
  - [Getting Start](#Getting-Start)
  - [Usage](#Usage)
  - [Demo](#Demo)
  - [Note](#Note)
  - [Contact](#Contact)

# basic-flask-web-app

## About The Project

* This is a simple Flask Web Application project.

## Getting Started

This section describes what is required to run this project in local environments.

### Prerequisites

* Python
* Flask
* SQLAlchemy

All you need is Python. The version when I run is below.
```
$ python --version
Python 3.10.6
```

### Installation

1. Clone repository
```
$ git clone git@github.com:kbanchi-portfolio/basic-flask-web-app.git
```
2. Install package
```
$ pip install -r requirements.txt
```

### Update Multilingual Message

1. Create Pot file
```
$ pybabel extract -F ./config/babel.cfg -k lazy_gettext -o ./config/messages.pot .
```
2. Create Multilingual file
```
$ pybabel init -i ./config/messages.pot -d translations -l ja
$ pybabel init -i ./config/messages.pot -d translations -l en
```
3. Update Multilingual file
```
$ pybabel update -i ./config/messages.pot -d translations
```
4. Set Multilingual messages
```
$ vi ./translations/ja/LC_MESSAGES/messages.po
$ vi ./translations/en/LC_MESSAGES/messages.po
```
5. Compile
```
$ pybabel compile -f -d translations
```

## Usage

Please refer to the help documentation how to use each module.

## Demo

[![basic-flask-web-app](http://img.youtube.com/vi/j68eRObCV-Q/sddefault.jpg)](https://www.youtube.com/watch?v=j68eRObCV-Q)

## Contact

kbanchi - [@kbanchi11](https://twitter.com/kbanchi11) - kbanchi@joatechnology.com

Project Link: [https://github.com/kbanchi-portfolio/](https://github.com/kbanchi-portfolio/)

## License

This project is licensed under the MIT License - see the [LICENSE.md](./LICENSE.md) file for details.

MIT License is a permissive license that is short and to the point. It lets people do anything they want with your code as long as they provide attribution back to you and don’t hold you liable.