# Apple .p12

A bot to change .p12 file password and checked its signed or revoke status.

## 📋 Requirements

- **Operating System:** Ubuntu 20.04 (Tested)
- **Languages & Libraries:**
  - Python 3
  - Node.js
- **Packages:**
  - aiogram

## 🔧 Installation

Follow the steps below for a smooth installation:

1. **System Update:**
    ```bash
    apt update && apt upgrade -y
    ```

2. **Installing Dependencies:**
    ```bash
    apt install openssl python3.11 python3-pip -y
    ```

3. **Installing Python Packages:**
    ```bash
    pip3 install aiogram
    ```

## ⚙️ Setup & Configuration

1. **Clone the Bot from GitHub:**  
    (Make sure to replace 'YOUR_REPO_LINK' with the actual link to the repository)
    ```bash
    git clone YOUR_REPO_LINK
    ```

2. **Navigate to the Bot Directory:**
    ```bash
    cd bot  
    ```

3. **Run the Node.js for P12 Checker:**
    ```bash
    node checker/resources.js
    ```

4. **Edit Configuration:**
    - Open the `bot.py` file using a text editor of your choice.
    - Locate and replace the bot token placeholder with your actual token.

5. **Run the Bot:**  
   You can either run the bot directly:
    ```bash
    python3 bot.py
    ```
   Or, to ensure the bot keeps running after you exit your Linux server session, use the `screen` command:
    ```bash
    screen -dmS bot python3 bot.py
    ```

Enjoy and contribute to make it even better! 🚀
