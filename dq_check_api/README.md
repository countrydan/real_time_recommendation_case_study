# Data Quality Check API Documentation

This API is responsible for validating data received from another system.

After validation the data gets a boolean flag indicating its validity. An assumption was made that no data should be rejected, rather flagged.

From here the validated data could be sent to another API or a messaging queue for further processing.

The API receives and processes data asynchronously, meaning that while its idle or waiting for I/O it can process data in the backlog.

# Assumption

 - any null value is not valid
 - review score has to be in the range of 1-5

# Further improvements

The review text can be limited, but this should be discussed with knowledge holders, as truncating this text might lead to valuable information loss.
On the other hand serializing and deserializing huge chunks of text data over and over again might slow down the system.

Other improvements include:
 - logging
 - further separation of responsibilities
## Setup Instructions

Build an image from the provided docker file:
   ```bash
   docker build -t myimage .
   ```
Start a container:
   ```bash
   docker run -d --name myimagecont -p 80:80 myimage
   ```
and the endpoints should be available at localhost.

Alternatively, install the required Python version (3.11), the dependencies and run the uvicorn command.
   ```bash
   uvicorn src.main:app
   ```

The API will now be running locally on port 8000 by default.
## Endpoints

### Receive data

- **URL:** `/receive`
- **Method:** POST
- **Description:** Receive new data.
- **Request Body:**
  ```json
  {
      "customer_id": 1,
      "service_id": 2,
      "timestamp": "2024-02-15",
      "review_txt": "test",
      "review_score": 2
  }
  ```
- **Response Body (Success, 201):**
  ```json
  {
      "msg": "received"
  }
  ```