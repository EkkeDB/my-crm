
import requests
from django.core.management.base import BaseCommand
from webapp.models import Cryptocurrency, HistoricalCryptocurrency
from reversion import revisions as reversion


class Command(BaseCommand):
    help = 'Fetches cryptocurrency data from an API and updates the database'

    def handle(self, *args, **kwargs):
        self.fetch_new_crypto_data()

    def fetch_new_crypto_data(self):
        # Example API endpoint for cryptocurrency data
        url = 'https://api.coingecko.com/api/v3/coins/markets'
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 10,
            'page': 1,
            'sparkline': 'false'
        }
        response = requests.get(url, params=params)
        new_data = response.json()

        # Archive old data
        old_data = Cryptocurrency.objects.all()
        for crypto in old_data:
            HistoricalCryptocurrency.objects.create(
                name=crypto.name,
                symbol=crypto.symbol,
                current_price=crypto.current_price,
                market_cap=crypto.market_cap,
                total_volume=crypto.total_volume,
            )

        # Update or insert new cryptocurrency data
        for crypto_data in new_data:
            self.update_or_insert_crypto(crypto_data)

    def update_or_insert_crypto(self, crypto_data):
        # Check if cryptocurrency with the same name already exists
        existing_crypto = Cryptocurrency.objects.filter(name=crypto_data['name']).first()

        if existing_crypto:
            # Update existing cryptocurrency entry
            with reversion.create_revision():
                existing_crypto.symbol = crypto_data['symbol']
                existing_crypto.current_price = crypto_data['current_price']
                existing_crypto.market_cap = crypto_data['market_cap']
                existing_crypto.total_volume = crypto_data['total_volume']
                existing_crypto.save()
                reversion.set_comment("Updated cryptocurrency data")
        else:
            # Create new cryptocurrency entry
            with reversion.create_revision():
                Cryptocurrency.objects.create(
                    name=crypto_data['name'],
                    symbol=crypto_data['symbol'],
                    current_price=crypto_data['current_price'],
                    market_cap=crypto_data['market_cap'],
                    total_volume=crypto_data['total_volume'],
                )
                reversion.set_comment("Added new cryptocurrency")