# ProTReND

## ProTReND web application

### Architecture
ProTReND web application is a django project based on the Architecture pattern proposed by Octoenergy 
and explained James Beith. 
For more detail, please refer to 
https://github.com/octoenergy/conventions/blob/master/patterns.md 
and https://www.jamesbeith.co.uk/blog/how-to-structure-django-projects/

In short, the project is different from the common Django apps structure. In contrast,
this project uses a clear separation between four core layers:

- **data** - The data model. It includes the Neo4j data models 
based on django-neomodel/neomodel OGM. It also includes the common django Models ORMs for a MySQL dbms.

- **interfaces** - The purpose of the interfaces layer is to validate input, call the domain or application layer, 
and return output. It links a given request to the respective business logic action 
- encoded into the application- or domain-layer. The API interface sub-app calls directly the domain layer.

- **application** - It contains the several use cases of the whole web application. Use-cases are the actions that the application provides 
such as creating a new TRN, building a TFBS dataset, etc.

- **domain** - Re-usable business logic. It implements universal queries and operations to the databases.


## Known Issues and Limitations

### ProTReND domain layer
The ProTReND domain layer has the following limitations:
- **TFBS Update** - update operations on binding sites are not possible due to missing logic. An error is raised
- **RegulatoryInteraction Update** - update operations on interactions are not possible due to missing logic. 
An error is raised
- **Relationship Create** - It is not currently possible to create arbitrary relationships between objects. 
Only read procedures are supported on nodes relationships. 
Although, upon creating binding sites and interactions new relationships are automatically created among these objects