# serverless-gemini-chatbot - A Client-Side Vertex AI Chatbot
A chatbot running with JS on the browser-client-side using a Google Cloud Run Function as proxy to Vertex AI (Gemini). 

IMPORTANT: Read the security information at the end of this README!

## 💬 Short Description

This is a chatbot that runs entirely in the user's browser (client-side) using JavaScript. It communicates with Google Cloud's Vertex AI API (Gemini model) via a server-side proxy function running on Google Cloud Run.

* **Frontend:** Pure JavaScript (or specify your framework, e.g., React, Vue, Svelte)
* **Backend/Proxy:** Google Cloud Run function (e.g., written in Node.js, Python, Go - specify the language)
* **AI Model:** Google Vertex AI (Gemini)

![image](https://github.com/user-attachments/assets/e4d131ed-0552-4f17-9f3c-926b5f0acac9)

You can test how it works on http://www.storz.net.

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

## Security Considerations: Protecting the Cloud Function Endpoint

This project utilizes a client-side JavaScript chatbot interface that communicates with a Google Cloud Function (`[Your Function Name, e.g., Gemini Proxy]`). This function acts as a backend proxy, forwarding requests to a paid Large Language Model service (e.g., Gemini via Vertex AI).

**WARNING: Critical Security Concern**

The URL endpoint of the deployed Cloud Function might be publicly discoverable by inspecting the website's client-side source code. If this endpoint is left unsecured, it creates significant risks:

1.  **Unauthorized Access:** Anyone who finds the URL can send requests directly to your Cloud Function, bypassing your website entirely.
2.  **Billing Abuse:** Since the Cloud Function calls a paid LLM service using your credentials, unauthorized requests can lead to unexpected and potentially substantial costs billed to your Google Cloud account.
3.  **Automated Abuse (Bots):** Malicious bots could flood your endpoint with requests, causing high costs and potentially disrupting the service.

**Mitigation Strategy: Server-Side Protection**

To protect your function and control costs, it is **essential** to implement security measures **on the server-side** (within the Cloud Function code or using Google Cloud infrastructure). Client-side checks alone are insufficient as they can be easily bypassed.

A layered approach is recommended:

1.  **CORS (Cross-Origin Resource Sharing):**
    * **Action:** Configure your Cloud Function to only allow requests originating from your specific website domain(s) by setting the `Access-Control-Allow-Origin` HTTP header appropriately.
    * **Purpose:** Prevents *other websites'* JavaScript from calling your function via a user's browser.
    * **Limitation:** Does **not** block direct server-to-server calls (e.g., using `curl`, scripts) or other non-browser clients.

2.  **reCAPTCHA v3 Verification (Strongly Recommended, this is what I use on my website http://www.storz.net):**
    * **Action:**
        * Integrate reCAPTCHA v3 (or Enterprise) on your website frontend. Register your domain(s) with Google to get a site key (public) and secret key (private).
        * Modify the client-side JavaScript to obtain a reCAPTCHA token when the user sends a message.
        * Send this token along with the user's prompt to the Cloud Function.
        * **Crucially:** Implement verification logic *within the Cloud Function*. Before calling the LLM, the function must make a server-side call to the Google reCAPTCHA `siteverify` API endpoint, sending its secret key and the received token.
    * **Purpose:** Verifies that the request likely originates from a human user interacting with your registered domain, effectively blocking most bots and automated scripts. This strongly "ties" the backend function to legitimate frontend usage.
    * **Action on Failure:** Reject requests that have missing, invalid tokens, or (for v3) a score below your defined threshold.

3.  **Rate Limiting:**
    * **Action:** Implement limits on the number of requests allowed from a single source (e.g., IP address) within a specific time window.
    * **Purpose:** Protects against brute-force or high-volume attacks from individual sources.
    * **Implementation:** Consider using Google Cloud Armor in front of your Cloud Run service for robust rate limiting capabilities.

4.  **Monitoring and Budget Alerts:**
    * **Action:**
        * Regularly monitor your Cloud Function logs and metrics (invocations, errors, execution times) for anomalies.
        * **Set up Google Cloud Billing budget alerts** for your project to receive immediate notifications if costs approach or exceed predefined thresholds.
    * **Purpose:** Provides visibility into usage patterns and acts as a critical safety net against unexpected billing.

5.  **(Optional) Authentication:**
    * **Action:** For higher security needs, implement user authentication (e.g., using Firebase Authentication or Google Identity Platform). Require requests to the Cloud Function to include a valid, server-verified identity token (e.g., JWT).
    * **Purpose:** Ensures requests come only from known, logged-in users.

**Conclusion:**

Implementing robust server-side security, particularly **reCAPTCHA verification** and **billing alerts**, is vital for the safe operation of this chatbot project. Do not deploy publicly without securing the Cloud Function endpoint.
---


