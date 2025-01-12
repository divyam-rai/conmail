# ConMail

This project aims to implement a Contact Mailer which would allow for bulk email sending to groups of contacts managed by the system. This was started with the goal of applying and developing skills across several technologies including: Kafka (with Schema Registry), Flink, ClickHouse, ElasticSearch as well as patterns such as CDC.

The system in question seemed to be simple enough to not be boggled down in the functional details of the system, and focus on experimenting with these technologies. The technologies would be integrated into the platform as follows:

- Kafka: Event messaging system which would be notified whenever an operation occurs on a contact or an organization.
- Flink: Perform real time analytics and store these in Clickhouse that would allow users to have realtime analytics on the contacts created, mails sent etc
- ElasticSearch: Allowing for full text search on the contacts imported by the user.

The project would further be deployed using Kubernetes (with the deployment files included in this repository) and currently implements the following services:

- **Contacts Service:** Provides the CRUD endpoints for managing contacts and organizations.
- **Protos Service:** Provides the Protobuf definitions required by the project. This was required as we would be integrating the Schema Registry using protobuf serialisation.

with more services that would be added as the project progresses.