# BusyBear 🐻

[![Talk with the early test version!](https://img.shields.io/badge/Deployed-green?style=flat-square&logo=telegram)](https://t.me/busybearbot)

I'm a Telegram bot that helps users with bus information in University of São Paulo (USP). 

BusyBear uses the SPTrans API to calculate the best stop point for the user to take, based on their location and the direction of the buses, in order to reduce the wait time in the points.

## Getting Started

1. Clone the repository: `git clone git@github.com:josemayer/busybear.git`

2. Install the required dependencies: `pip install -r requirements.txt`

3. Create a .env file based on .env.sample and set the environment variables with your keys.

4. Run the bot: `python main.py`

### Deployment

This bot has currently an early test version deployed and running at `@busybearbot` Telegram username. You can test it by clicking the green flag above the first section.

If you want to deploy your own instance of the bot, please follow the steps outlined in the [Getting Started](#getting-started) section. Once you have set up the environment variables with your own API keys, you can run the bot.

## Usage

- Send the command `/start` to the bot to get a greeting message.
- Send the command `/list_buses <way>` to the bot to get buses and its stops at moment.
- Send your location to the bot to get distances from points within a 250 meter radius.

## Built With

- [Python](https://www.python.org/) - Programming language used
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Library used for building Telegram bots in Python

## Contributing

You can contribute to this project by submitting a pull request.

## Authors

- **José Lucas Silva Mayer** - *Initial work*

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

