# serverless-gemini-chatbot - A Client-Side Vertex AI Chatbot
A chatbot running with JS on the browser-client-side using a Google Cloud Run Function as proxy to Vertex AI (Gemini). 

## 💬 Short Description

This is a chatbot that runs entirely in the user's browser (client-side) using JavaScript. It communicates with Google Cloud's Vertex AI API (Gemini model) via a server-side proxy function running on Google Cloud Run.

* **Frontend:** Pure JavaScript (or specify your framework, e.g., React, Vue, Svelte)
* **Backend/Proxy:** Google Cloud Run function (e.g., written in Node.js, Python, Go - specify the language)
* **AI Model:** Google Vertex AI (Gemini)

*(Optional: Add a screenshot or GIF of the chatbot in action here)*
## ✨ Features

* Interactive chat interface in the browser.
* Leverages the powerful Gemini models via Vertex AI.
* Secure communication: API keys or service account credentials are not exposed in the frontend but are securely managed in the Cloud Run proxy.
* Scalable backend infrastructure thanks to Cloud Run.

## 🏛️ Architecture

The communication flow is as follows:

1.  **Browser (Client-Side JS):** Sends the user input to the Cloud Run Proxy URL.
2.  **Google Cloud Run (Proxy):** Receives the request, adds the necessary authentication for Vertex AI (e.g., API key or service account token), and forwards the request to the Vertex AI API.
3.  **Google Vertex AI (Gemini):** Processes the request and sends the response back to the Cloud Run function.
4.  **Google Cloud Run (Proxy):** Receives the response from Vertex AI and forwards it back to the browser.
5.  **Browser (Client-Side JS):** Displays the chatbot's response.

## ⚙️ Prerequisites

Before you begin, ensure you have the following installed and set up:

* A Google Cloud Platform (GCP) account with billing enabled.
* [Google Cloud SDK (`gcloud` CLI)](https://cloud.google.com/sdk/docs/install) installed and configured (`gcloud init`).
* [Python](https://www.python.org/) (e.g., version 3.9 or later) and pip.
* Necessary Google Cloud APIs enabled in your project (at least: Vertex AI API, Cloud Run API, Cloud Build API - if using Cloud Build for deployment).
* A service account with the required permissions for Vertex AI (e.g., "Vertex AI User") - *or* an API key if you prefer that approach (less recommended for Cloud Run).

## 🚀 Setup & Installation

The setup involves two parts: deploying the proxy function and configuring the frontend.

### 1. Backend (Cloud Run Proxy)

*(Steps to set up and deploy the Python Cloud Run function):*

1.  **Clone the repository:**
    ```bash
    git clone [https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories)
    cd [directory containing your Cloud Run function code]
    ```
2.  **Dependencies:**
    * Ensure your Python dependencies are listed in a `requirements.txt` file in the same directory as your main Python code (e.g., `main.py`). Cloud Build will use this file during deployment.
    * *(Optional - For local testing):* Create a virtual environment and install dependencies locally:
      ```bash
      python -m venv venv
      source venv/bin/activate  # On Windows use `venv\Scripts\activate`
      pip install -r requirements.txt
      ```
3.  **Configuration:**
    * Ensure your Python code can access the GCP Project ID and region if needed (often available via environment variables automatically set by Cloud Run).
    * Ensure your function has access to Vertex AI credentials. The recommended way is to run the Cloud Run service with a specific service account that has the necessary Vertex AI permissions (e.g., "Vertex AI User" role). You set this during deployment (`--service-account` flag). Avoid hardcoding keys directly in the code.

4.  **Deploy to Cloud Run:**
    * Use the `gcloud` CLI to deploy directly from your source code. Cloud Build will automatically detect your `requirements.txt` file, install dependencies, and build the container image.
    ```bash
    gcloud run deploy [SERVICE_NAME] \
        --source . \
        --platform managed \
        --region [YOUR_REGION] \
        --allow-unauthenticated \
        --project=[YOUR_GCP_PROJECT_ID]
        # --- Add Python specific options if needed ---
        # E.g., specify runtime if needed: --runtime python311
        # E.g., specify service account for credentials: --service-account [YOUR_SERVICE_ACCOUNT_EMAIL]
        # E.g., set environment variables: --set-env-vars KEY1=VALUE1,KEY2=VALUE2
    ```
    * **Note:** Replace `[SERVICE_NAME]`, `[YOUR_REGION]`, `[YOUR_GCP_PROJECT_ID]`, and optionally `[YOUR_SERVICE_ACCOUNT_EMAIL]` with your specific values.
    * **Take note of the outputted Service URL**. You will need this for the frontend configuration.

### 2. Frontend (Client-Side JavaScript)

1.  **Clone the repository (if not already done):**
    ```bash
    git clone [https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories)
    cd [directory of the frontend]
    ```
2.  **(Optional) Install dependencies:**
    ```bash
    # Example: npm install (if you use bundlers like Webpack/Vite)
    ```
3.  **Configuration:**
    * Open the relevant JavaScript file (e.g., `script.js`, `config.js`, or similar).
    * Find the variable storing the backend URL and insert the URL of your deployed Cloud Run function:
        ```javascript
        const CLOUD_RUN_PROXY_URL = 'YOUR_CLOUD_RUN_URL_HERE';
        ```
4.  **Run:**
    * Open the `index.html` file directly in your browser.
    * *Or* if you are using a local development server:
        ```bash
        # Example: npm run dev
        ```

## 🛠️ Usage

After completing the setup:

1.  Open `index.html` in your browser (or the URL of your local development server).
2.  Type your messages into the chat input field and press Enter or click "Send".
3.  The response from Vertex AI (Gemini) should appear in the chat window.

## 📝 License

This project is licensed under the [MIT License](LICENSE) (or your chosen license).

## 🙌 (Optional) Contributing

Contributions are welcome! Please read `CONTRIBUTING.md` for details on our code of conduct and the process for submitting pull requests.

---


