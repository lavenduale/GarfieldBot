from GarfieldBot import GarfieldPlugin, MessageEvent
from dotenv import load_dotenv, find_dotenv
import praw
import os

class RedditPlugin(GarfieldPlugin):
    """ Get top 5 articles from a given subreddit and display 5 comments from the articles """

    def __init__(self, manifest, bot):
        super().__init__(manifest, bot)
        
        # Login with details from env
        load_dotenv(find_dotenv())
        self.reddit = praw.Reddit(
            client_id       = os.environ["REDDIT_CLIENT_ID"],
            client_secret   = os.environ["REDDIT_CLIENT_SECRET"],
            username        = os.environ["REDDIT_USERNAME"],
            password        = os.environ["REDDIT_PASSWORD"],
            user_agent      = 'GarfieldBotRedditPlugin'
        )

        # Register commands
        self.bot.register_command("reddit", self.handle_reddit)
        self.bot.register_command("comments", self.handle_comments)

    def handle_reddit(self, event: MessageEvent, *args) -> None:
        # Create a reference to the subreddit specified
        subreddit = self.reddit.subreddit(args[0])
        
        # Get the top 5 submissions of the day
        links = 1
        for submission in subreddit.top('day'):
            # Skip all submissions tagged NSFW
            if(submission.over_18):
                continue
            
            # Build the message for the channel
            message = "!comments " + str(submission.id) + " *" + str(submission.title) + "*\n" + str(submission.url)

            self.bot.send_message(event.channel, message)
            links += 1
            
            # Stop after 5 links
            if(links > 5):
                break

    def handle_comments(self, event: MessageEvent, *args) -> None:
        # Get a reference to the submission, and also to the comments
        submission = self.reddit.submission(args[0])
        submission_comments = submission.comments.list()

        # Make sure the comments are actually comments
        real_comments = [
            comment
            for comment
            in submission_comments
            if isinstance(comment, praw.models.Comment)
        ]

        # Get the top five comments
        real_comments.sort(
            key=lambda comment: comment.score, reverse=True
        )
        top_comments = real_comments[:5]

        # Add the comments as a thread to the submission        
        for comment in top_comments:
            realcomment = "_*" + str(comment.author) + "*_: " + str(comment.body) + "\n"
            
            self.bot.send_to_thread(
                event.channel, event.ts, str(realcomment)
            )

