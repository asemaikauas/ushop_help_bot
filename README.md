<a id="readme-top"></a>

<div align="center">
  <h3 align="center">Ushop Support Bot</h3>
  <p align="center">
    Bilingual Telegram assistant that helps users resolve order, payment, and return issues by guiding them through a dynamic menu while routing complex queries to human managers
    <br />
    <br />
    <a href="https://t.me/ushop_help_bot">Test Bot</a>
    <br />
    <a href="https://youtu.be/5MQqVLDl57s">View Demo</a>
  </p>
</div>

---

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#demo">View Demo</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

---

## About The Project


**Ushop Market Support Bot** is a Telegram bot that provides automated customer support for Ushop Market users in Kazakh and Russian. It helps customers resolve common issues related to orders, deliveries, payments, returns, and promotions, while routing complex queries to human managers.

It includes: 
- Language Selection: Supports both Kazakh and Russian.
- Order Help: Delivery tracking, returns, and item-related inquiries.
- Promo & Payment Help: Troubleshoots issues with promo codes and payment.
- Human Escalation: Collects necessary info and sends it to a manager group chat in the cases of complex queries that cannot be addressed by bot.
- Modular Support Menu: Clear buttons for 20+ support cases.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---


### Built With

* [Python 3](https://www.python.org/)
* [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/)
* Telegram Bot Platform
* Inline Keyboards & Callback Queries

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Getting Started

### Prerequisites

You’ll need:
- Python 3.8+
- Telegram Bot Token
- A Telegram group (to send manager alerts)

---
### Installation

1. Clone the repo
   
   ```bash
   git clone https://github.com/asemaikauas/ushop-help-bot.git
   cd ushop-help-bot
   ```

2. Pip install pyTelegramBotAPI

3. Create a `.env` file in the root directory with your bot token:
   
   ```bash
   TELEGRAM_API_KEY=your_bot_token_key
   ```

4. Run the bot:
   
   ```bash
   python bot.py 
   ```


## Usage

1. Click **Start**.
2. Choose your preferred language (Kazakh or Russian).
3. Select a question from the menu:
   - 📦 Order issues
   - 🔧 Changing or canceling orders
   - 💸 Payment or returns
   - 🤝 Cooperation or becoming a seller

4. The bot will guide you through a dynamic conversation - ask questions, answer them instantly - and forward complex responses to the manager group chat for support.


<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Demo

Watch a quick walkthrough of the application:

[[Watch the demo]](https://youtu.be/5MQqVLDl57s)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


---

## Roadmap

 - Add admin dashboard to review queries
 - Implement logging for analytics
 - Add English language support

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Contributing

Contributions are what make the open source world amazing!  

1. Fork the repo  
2. Create a feature branch  
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes  
4. Push and open a PR  
5. 🌟 Star the project!

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Contact

Asemai – kauasasemai05@gmail.com  
Project Link: [ushop_bot](https://github.com/asemaikauas/debatelink)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Acknowledgments

- 🤖 [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) — for simplifying Telegram bot development
- 🌐 [Telegram Bot Platform](https://core.telegram.org/bots) — for API docs and bot setup
- 🧰 [dotenv](https://pypi.org/project/python-dotenv/) — for managing API keys securely



<p align="right">(<a href="#readme-top">back to top</a>)</p>
