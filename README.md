# Name Classification API (FastAPI)

## 📌 Overview

This project implements a high-performance REST API using **FastAPI** that classifies a given name by gender using the external Genderize API. The service processes and enriches the raw response with additional logic to provide a structured and reliable output.

The API is designed with scalability, robustness, and clean architecture in mind, making it suitable for production-grade use cases.

---

## 🚀 Features

* Fast and asynchronous API built with FastAPI
* External API integration (Genderize)
* Data transformation and enrichment
* Confidence scoring logic
* Consistent error handling
* CORS-enabled for cross-origin access
* Production-ready structure

---

## 📡 Endpoint

### Classify Name

**GET** `/api/classify?name={name}`

#### Example Request

```
/api/classify?name=john
```

#### Success Response (200 OK)

```json
{
  "status": "success",
  "data": {
    "name": "john",
    "gender": "male",
    "probability": 0.99,
    "sample_size": 1234,
    "is_confident": true,
    "processed_at": "2026-04-01T12:00:00Z"
  }
}
```

---

## 🧠 Processing Logic

The API performs the following transformations on the Genderize response:

* Extracts:

  * `gender`
  * `probability`
  * `count` → renamed to `sample_size`
* Computes:

  * `is_confident = true` if:

    * `probability ≥ 0.7`
    * `sample_size ≥ 100`
* Adds:

  * `processed_at` timestamp (UTC, ISO 8601 format)

---

## ⚠️ Error Handling

All errors follow a consistent structure:

```json
{
  "status": "error",
  "message": "<error message>"
}
```

### Error Cases

| Status Code | Condition                                           |
| ----------- | --------------------------------------------------- |
| 400         | Missing or empty `name` parameter                   |
| 422         | No prediction available (null gender or zero count) |
| 502         | External API failure                                |
| 500         | Internal server error                               |

---

## 🔍 Edge Cases

* If `gender = null` OR `count = 0`, the API returns:

```json
{
  "status": "error",
  "message": "No prediction available for the provided name"
}
```

---

## 🛠️ Tech Stack

* **FastAPI** — Web framework
* **httpx** — Async HTTP client
* **Uvicorn** — ASGI server

---

## ▶️ Running Locally

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/name-classification-api.git
cd name-classification-api
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Server

```bash
uvicorn main:app --reload
```

### 4. Test the API

```
http://127.0.0.1:8000/api/classify?name=john
```

---

## 🌐 Deployment

This API can be deployed on platforms such as:

* Railway
* Vercel (with configuration)
* Heroku
* AWS

### Recommended Start Command:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## 📈 Performance Considerations

* Asynchronous request handling ensures high concurrency
* External API calls are non-blocking
* Lightweight processing ensures sub-500ms internal response time

---

## 👤 Author

**Arowosaye Victor Oluwadamilola**