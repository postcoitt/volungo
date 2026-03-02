**VOLUNGO**

---

## About the Project

Volungo is a modern web platform designed to connect volunteers with social organizations and nonprofit initiatives. It brings the power of social networking to the volunteer and NGO ecosystem, enabling meaningful interactions, project discovery, community growth, and real-world impact.

The platform is focused on building a socially connected volunteer community where:
* **Individuals** passionate about volunteering can discover meaningful opportunities, connect with nonprofits and NGOs, share experiences and stories, and track their participation and contributions.
* **Organizations** can publish volunteer projects, manage volunteer applications, build an engaged community, and share updates and media.

**Our Mission:** To empower volunteers and social entities to create positive societal change through an intuitive, accessible, and community-driven platform.

---

## Key Features

**Role-Based Authentication:** Secure user authentication with distinct flows for Volunteers and Organizations.
**Profile & Activity Management:** Dedicated user profiles with avatars, personal info, and tracking of volunteer activities.
**Project Management for NGOs:** Organizations can easily post, update, and manage social initiatives and track applications.
**Smart Discovery:** Searchable volunteer opportunities with advanced filtering options.
**Map Integration:** Visual discovery of nearby volunteering events via the `mapapp` module.
**Social Engagement:** Interact with the community through posts, comments, and connections.
**Mobile-First Responsive UI:** A seamless experience across desktop, tablet, and mobile devices.
**RESTful API:** Ready for modern frontend frameworks or mobile application integrations.

---

## Tech Stack

Volungo is built using a robust and scalable stack, leveraging the latest version of Django (6.0+).

| Layer      | Technology                                                                                               |
| ---------- | -------------------------------------------------------------------------------------------------------- |
| **Backend** | Python 3, Django 6.0.2                                                                                   |
| **Frontend** | HTML5, CSS3, Django Templates                                                                            |
| **Database** | PostgreSQL (Production) / SQLite3 (Development)                                                          |
| **API** | Django REST Framework (DRF)                                                                              |
| **Auth** | Django Session Auth / Custom User Models                                                                 |

---

## Project Structure

The project follows an advanced Django architectural pattern, separating configuration (`core`) from business logic apps (`volungo`).

```text
volungo.git/
├── core/                   # Main Django configuration directory
│   ├── __init__.py
│   ├── asgi.py             # ASGI config for async web servers
│   ├── settings.py         # Primary settings (apps, middleware, DB, static/media)
│   ├── urls.py             # Root URL routing
│   └── wsgi.py             # WSGI config for deployment
├── volungo/                # Business logic and Django Apps container
│   ├── accounts/           # User authentication and registration logic
│   ├── avatars/            # Profile picture handling
│   ├── mapapp/             # Geospatial and mapping features for opportunities
│   └── users/              # Core user models and profiles
├── media/                  # User-uploaded files (avatars, project images)
├── static/                 # CSS, JavaScript, and global images
├── .gitignore              # Ignored files and directories
├── manage.py               # Django command-line utility
└── README.md               # Project documentation
