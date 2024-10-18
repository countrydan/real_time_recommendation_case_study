# Real time recommendation case study
## Requirement:

### Part 1:

The client wants to reduce the impact of negative experiences of its customers, so it provides the opportunity to provide feedback through a channel identified through the application.
The application generates a JSON file that contains, among other things, the customer ID, the service ID, the time, the textual rating and the score value (on a scale of 1-5)

The application developers ask us to define the channel through which the messages are delivered to us.
It is important to handle every event and respond to every critical rating.

In the case of critical ratings, our task is to offer the customer a discount using the customer’s details, profile and a continuously updated database of discounts and pass it on to the application that writes the message, which encapsulates the message in a complete sentence. We must post this offer on a channel that will definitely send it to the processing system as soon as possible.

### Part 2:

Implement an application that receives the received JSON file based on the previously defined information and performs data validation on it:
- What data validation should be performed?
- Are missing values allowed ​​and if so, how would you handle them?
- Writing unit tests to verify functionality

## Solution to part 1

### Case study summarization:
A JSON message received with a score ranging from 1-5 along with various other fields.
The assumption is that critical messages are ones that have scores 1-3. These must be responded with a custom offer as soon as possible. Besides that, all events must be handled, acknowledgment from sending the custom offer must be received.

### Proposed solution:
For this use case Apache Kafka offers a lot of benefits. Kafka can be easily scaled horizontally, ensuring high throughput throughout the project's life cycle.Through broker distribution and additional consumers high availability and fault tolerance can be achieved. By creating partitions in a topic, processing can be parallelized, thus speeding up reacting to critical messages.

For ingestion and processing REST APIs can be implemented. REST APIs offer flexibility by allowing each service to have their own API. These APIs in the beginning could be implemented in a language that is good for prototyping and fast code production (e.g. Python, Javascript). Later they could be reimplemented in a more performant and more maintainable language (e.g. Java, Rust).

![proposed architecture](https://github.com/countrydan/real_time_recommendation_case_study/blob/main/case_study.jpg)

### Workflow:
The JSON is received from the application to a REST API. The API sends the data to the first broker according to its topic and partition if it has. This API could also be responsible for data quality checks, although this could be a separate service. 
By splitting up the responsibilities further parallelization could be achieved. For example if the receiving API would categorise the messages according to their score, the critical scores could each have their own API or processes doing the data quality check and then writing to the first broker’s partitions.
Another approach could be that the application producing the JSON already knows about the topics and partitions, so it could directly send messages to a broker similar to the first one in the picture. From there a consumer group could get the messages, do the data quality checks and publish to a broker with partitions.

The topics and partitions are determined by the criticality of the message. If the message has a score of 4 or 5 it goes to a topic handling only these two categories. Since it is not required to react to these messages, they can be sent to a consumer that persists it and does a batch processing job periodically (again, this could be a separate service).

For the critical messages (1-3) there is a separate topic with three additional partitions, each partition corresponds to its score. By having these partitions a consumer group can be created with three processes consuming from the partitions parallelly. These processes query a Cassandra database retrieving all necessary information and with possibly a machine learning model choose the best fitting discount/promotion for the customer. By having Cassandra with as many nodes as partitions, in this case 3, parallelization could be kept at maximum. Customer details could be refreshed by an ETL job or if required with CDC. The discount name or id could be attached to the json and be sent to the second broker where there are 3 partitions again.

From the second broker the final service layer can consume from all partitions. This could also be parallelized by having 3 service layer processes.
