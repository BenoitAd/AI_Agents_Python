# API AI Agent Against Hateful Messages on Social Media

## Introduction
This API is designed to assist victims of hateful or criminal messages on social media. It leverages the OpenAI API and AI agents to respond to user questions regarding harmful messages in various contexts, including legal, emotional support, and cybersecurity.

## Features
- **Legal Expertise**: An AI agent provides legal advice on how to respond to harmful messages, based on local laws and regulations.
- **Emotional Support**: An AI agent offers emotional support by responding in a comforting and supportive manner.
- **Cybersecurity Advice**: For cases involving fraudulent activities, an AI agent gives practical cybersecurity guidance on best practices.

## Requirements
- Docker
- python-dotenv==1.0.1
- Flask==2.2.5
- crewai==0.70.1

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/BenoitAd/AI_Agents_Python.git
2. Create a .env file in the root of the project with the following variables:
  - OPENAI_API_KEY=YOUR_API_KEY
  - OPENAI_MODEL_NAME=MODEL
3. Create the docker image
   ```bash
   docker-compose up
The API will be available on port 5000.

## Usage

### Endpoints
- **POST** `/api/chat`

### Headers
- `Content-Type: application/json; charset=UTF-8`

### Example Request Body
```json
{
    "message": "User message",  // Copy of the hateful message from the user
    "agent": 3  // Agent selection: 1 = Legal, 2 = Emotional Support, 3 = Cybersecurity
}
```
**Explanation**:
- message: The harmful or hateful message the user has received.
- agent: Select which AI agent to use for the response:
  1: Legal advice.
  2: Emotional support.
  3: Cybersecurity advice.

### Configuration

- The AI agents are configured to respond in French. If you want the agents to reply in a different language, update their context in the `main.py` file by adjusting the relevant language settings.
  
- To change the API port, modify the `docker-compose.yml` file or the Dockerfile:
  - In `docker-compose.yml`, update the following line to set a new port:
    ```yaml
    ports:
      - "5000:5000"
    ```
    Replace `5000` with your desired port number.

  - Alternatively, in the Dockerfile, you can update the `EXPOSE` command if necessary:
    ```dockerfile
    EXPOSE 5000
    ```
    Replace `5000` with the port of your choice.


### Contact
For inquiries, contact me on Linkedin: https://www.linkedin.com/in/benoit-auger-dubois-788082276/
