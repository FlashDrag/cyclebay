# CycleBay

## Overview


Live Demo: https://cyclebay-bc1e75ddbf8e.herokuapp.com/

![mockup](docs/images/mockup.png)

## Table of Contents

## Agile Methodology
The main goal of the app is to deliver a solution that creates real value for the users and _UX design_ and _Agile Methodology_ are the best way to achieve this goal.

#### Project Goals
- Create a web application that allows users to buy bycicles online.


### Development process
This project was developed with the Agile methodology which allowed me to develop the app iteratively and incrementally, and adapt changes with flexibility even in the late stages of development.

_GitHub Issues_ and _Projects_ are used to manage the development process.

The Project link: https://github.com/users/FlashDrag/projects/11

Each siqnificant feature is presented as an _Epic_ and then broken down into smaller _User Stories_ that are then added to the _Project Backlog_. _Epics_ are marked with labels to indicate the feature. It allows me to filter the _User Stories_ by feature and then allocate them to _Milestones_ and prioritize them.

The _GitHub__ Kanban_ board is used to manage the process and track the progress of the development. When _User Story_ is created, it is automatically added to the _Backlog_ column to be prioritized. The product _Backlog_ is never complete, as it is a dynamic document to respond to changes effectively. As new features are identified, they are added to the product _Backlog_. As the product is released, the product _Backlog_ is constantly updated to reflect changes in the product and changes in the market. The Kanban board includes the following columns:
- **Backlog** - the list of all _User _Stories_ that have not yet been scheduled to be completed. As new _User Stories_ are created, they are automatically added to the _Backlog_ column.
- **Sprint Backlog** - the collection of prioritized _User Stories_ that have been selected for the current _Sprint_.
- **Development** - the user stories that are currently being developed.
- **Testing** - user stories that are currently being tested.
- **Done** - all completed and tested _User Stories_.


The Project Table is used to filter and then allocate _User Stories_ to _Milestones_ and prioritize them. At the start of each sprint, the _User_ Stories_ are selected from the _Backlog_ and added to the _Sprint Backlog_ with attached priority labels.
The _User Stories_ prioritized using the _MoSCoW_ method. The prioritization was based on the following criteria:
- **Must Have** - The _User Story_ is crucial and add significant value to the product and must be delivered in the current iteration.
- **Should Have** - The _User Story_ is important but not critical to the success. Simply delivery is not guaranteed within the current iteration.
- **Could Have** - The _User Story_ is desirable and would only be delivered in their entirety in a best-case scenario. When a problem occurs and the deadline is at risk, one or more could-have items are dropped.
- **Won't Have** - The _User Story_ will not be delivered in the current delivery timebox but may be considered for the future.
The prioritization is based on the 60-20-20 rule where 60% of the effort is spent on the Must Have, 20% on the Should Have and the rest 20% on the Could Have. When the Sprint starts, the _User Stories_ are moved to the _Development_ column, where first the Must Have items. When the development of a particular _User Story__ is completed, it is moved to the _Testing_ column, tested and then moved to the _Done_ column manually or using the _commit_ message concerning the User Story ID. If the time is running out and the _User Stories_ are not completed, the Could Have items are dropped back to the _Backlog_ column for re-prioritization.

*GitHub Kanban Board*
![GitHub Kanban Board](docs/images/Board.png)

*GitHub Project Table*
![GitHub Project Table](docs/images/Table.png)

*Milestones*
![Milestones](docs/images/Milestones.png)

[Back to top](#table-of-contents)


#### User Stories


## UX Design
### Structure
The CycleBay website is designed to be simple and easy to navigate. The site has a responsive design to provide an optimal viewing experience across a wide range of devices.

### Wireframes
The wireframes were created using [Balsamiq](https://balsamiq.com/). Here are some initial wireframes created at the beginning of the project. The final design may differ from the initial wireframes.

[Back to top](#table-of-contents)

### UI Design
#### Color Scheme
...

![color Palette](docs/images/Palette.png)

#### Typography

#### Styling

#### Images

[Back to top](#table-of-contents)

### Database Design
The Get Job platform uses a relational database to store and manage data. The RDBMS used for this project is [PostgreSQL](https://www.postgresql.org/) which is hosted on the cloud service [ElephantSQL](https://www.elephantsql.com/).

The ER Diagram below shows the structure of the database and the relationships between the tables. This diagram was created using [Microsoft Visio](https://www.microsoft.com/en-ie/microsoft-365/visio/).

![er_diagram](docs/images/erd.png)

[Back to top](#table-of-contents)

## Features
### Existing Features

### Future Features
...

[Back to top](#table-of-contents)

### Development Features
...

[Back to top](#table-of-contents)

## Database
The app uses a relational database service [ElephantSQL](https://www.elephantsql.com/) to store and manage data.

*Database Configuration*
```
development = os.getenv('DEVELOPMENT', False) == 'True'

if development:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    if os.getenv("DATABASE_URL", None) is None:
        raise Exception("DATABASE_URL environment variable not defined")

    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL')
        )
    }
```

*ElephantSQL Instance*
![Instances-ElephantSQL](docs/images/Instances-ElephantSQL.png)

[Back to top](#table-of-contents)

## Static Files
The static files are hosted on the cloud service [AWS S3](https://aws.amazon.com/s3/).

*AWS S3 Bucket*
![AWS S3 Bucket](docs/images/AWS-S3-Bucket.png)

[Back to top](#table-of-contents)

## Technologies Used
### Languages
- [HTML5](https://en.wikipedia.org/wiki/HTML5)
- [CSS3](https://en.wikipedia.org/wiki/CSS)
- [JavaScript](https://en.wikipedia.org/wiki/JavaScript)
- [Python](https://en.wikipedia.org/wiki/Python_(programming_language))
### Frameworks, Libraries
- [Django 3.2](https://docs.djangoproject.com/en/3.2/)
- [Bootstrap 5](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- [jQuery 3.6.4](https://releases.jquery.com/)
- [Font Awesome 6.4](https://fontawesome.com/)
- [Stripe](https://stripe.com/docs)
### Tools
- [Git](https://git-scm.com/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Microsoft Visio](https://www.microsoft.com/en-ie/microsoft-365/visio/)
- [Google Fonts](https://fonts.google.com/)
- [Heroku](https://www.heroku.com/)
- [AWS S3](https://aws.amazon.com/s3/)
- [Balsamiq](https://balsamiq.com/)
- [Sass](https://sass-lang.com/)
- ### Django packages
- [django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/)
- [cripsy-bootstrap5](https://github.com/django-crispy-forms/crispy-bootstrap5)
- [django-allauth](https://django-allauth.readthedocs.io/en/latest/)

## Testing
See [TESTING.md](https://github.com/FlashDrag/cyclebay/blob/master/docs/TESTING.md) for an overview of the app testing and debugging.

[Back to top](#table-of-contents)

## Deployment, CI/CD
The Get Job platform is deployed on the [Heroku](https://www.heroku.com/) cloud platform and can be accessed here https://cyclebay-bc1e75ddbf8e.herokuapp.com/

## Credits

## Contacts
If you have any questions about the project, or you would like to contact me for any other reason, please feel free to contact me by email or via social media.

[![Gmail Badge](https://img.shields.io/badge/-flashdrag@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:flashdrag@gmail.com)](mailto:flashdrag@gmail.com)

[<img src='https://img.shields.io/badge/Telegram-333333?style=for-the-badge&logo=telegram&logoColor=white&style=plastic&logoWidth=20&labelColor=2CA5E0' alt='Telegram'>](https://t.me/flashdrag) [<img src='https://img.shields.io/badge/LinkedIn-333333?style=for-the-badge&logo=linkedin&logoColor=white&style=plastic&logoWidth=20&labelColor=0077B5' alt='Telegram'>](https://www.linkedin.com/in/pavlo-myskov)

[Back to top](#table-of-contents)