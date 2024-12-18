import requests
from loguru import logger

class DiscordNotifier:

    def __init__(self, 
                 method:        str = 'webhook', 
                 webhook_url:   str = None, 
                 token:         str = None, 
                 channel_id:    str = None
                 ):

        """
        :param webhook_url: The URL of the Discord webhook
        :param method:      The method to use for the notification (e.g. 'api', 'webhook')
            api requires token and channel_id
            webhook requires webhook_url
        :param token:       The Discord token
        :param channel_id:  The Discord channel ID
        """
        self.method:        str = method
        self.webhook_url:   str = webhook_url
        self.token:         str = token
        self.channel_id:    str = channel_id

    def notify(self, msg):
        """
        Send a message to Discord
        :param msg: The message to send
        """
        if self.method == 'api':
            if self.token is None:
                logger.error("Token not set")
            elif self.channel_id is None:
                logger.error("Channel ID not set")
            else:
                self.notify_api(msg)
        elif self.method == 'webhook':
            if self.webhook_url is None:
                logger.error("Webhook URL not set")
            else:
                self.notify_webhook(msg)
        else:
            logger.error(f'Invalid method: {self.method}')    

    def notify_webhook(self, msg: str):
        """
        Send a message to Discord using a webhook
        :param msg: The message to send
        """
        headers = {"Content-Type": "application/json"}
        data = {"content": msg, "username": "newmanBot"}
        res = requests.post(self.webhook_url, headers=headers, json=data)
        if res.status_code in (200, 204):
            logger.info(f"Request fulfilled with response: {res.text}")
        else:
            logger.error(f"Request failed with response: {res.status_code}-{res.text}")
    
    def notify_api(self, msg):
        """
        Send a message to Discord using the API
        :param msg: The message to send
        """
        url_base = 'https://discord.com/api/v10'
        url = f'{url_base}/channels/{self.channel_id}/messages'
        headers = {
				"Authorization": f"Bot {self.token}",
				"Content-Type": "application/json"
		}
        data = {"content": msg}
        res = requests.post(url, headers = headers, json = data) 
        if res.status_code in (200, 204):
            logger.info(f"Request fulfilled with response: {res.text}")
        else:
            logger.error(f"Request failed with response: {res.status_code}-{res.text}")

if __name__ == '__main__':


    # enter your webhook url or token and channel id before running the script
    TEST_WEBHOOK_URL = ''
    CHANNEL_ID       = ''
    TOKEN            = ''

    """example of using the DiscordNotifier class with an API token"""
    # notifier = DiscordNotifier(method = 'api',token = TOKEN, channel_id = CHANNEL_ID)
    # notifier.notify("Hello, world!")

    """example of using the DiscordNotifier class with a webhook"""
    # notifier = DiscordNotifier(method = 'webhook', webhook_url = TEST_WEBHOOK_URL)
    # notifier.notify("Hello, world!")























