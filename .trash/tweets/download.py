from ntscraper import Nitter

scraper = Nitter(log_level=1, skip_instance_check=False)

print(scraper.get_tweets("weird_offspring", mode='user'))
