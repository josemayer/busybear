# BusyBear 🐻

I'm a Telegram bot that helps users with bus information in University of São Paulo (USP). 

BusyBear uses the SPTrans API to calculate the best stop point for the user to take, based on their location and the direction of the buses, in order to reduce the wait time in the points.

## Getting Started

1. Clone the repository: `git clone git@github.com:josemayer/busybear.git`

2. Install the required dependencies: `pip install -r requirements.txt`

3. Create a .env file based on .env.sample and set the environment variables with your keys.

4. Run the bot: `python main.py`

## Usage

- Send the command `/start` to the bot to get a greeting message.
- Send the command `/bus` to the bot to get bus stop recommendations based on your location.

## Built With

- [Python](https://www.python.org/) - Programming language used
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Library used for building Telegram bots in Python
- [TomTom](https://www.tomtom.com) - Mapping and geolocation data API

## Contributing

You can contribute to this project by submitting a pull request.

## Authors

- **José Lucas Silva Mayer** - *Initial work*

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

