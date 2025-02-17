### How to run
Below are the instructions to run your Spring Boot project:
Ensure Prerequisites are Installed

Java Development Kit (JDK): Make sure you have JDK 11 or later installed.
Maven: Ensure Maven is installed and available in your system's PATH.
Build the Project
Open a terminal in the project root (where your pom.xml file is located) and run:

    mvn clean install
    mvn spring-boot:run

### API Tables

| API Endpoint         | HTTP Method | Description                                                                  |
|----------------------|-------------|------------------------------------------------------------------------------|
| `/getUser`           | GET         | Retrieves a single user (currently returns user with id = 1).                |
| `/getAllUsers`       | GET         | Retrieves all users             |
| `/getAllExpenses`    | GET         | Retrieves all expenses from the database.                                  |
| `/getCategoryCounts` | GET         | Returns distinct expense categories along with their occurrence counts.      |

