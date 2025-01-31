"""
A class to prompt the OpenAI REST API
"""

from openai import OpenAI

from celebi.core.flask.config import AppConfig
from .prompt_response_pair import PromptResponsePair


class LLMPrompt:
    """
    Prompts the LLM using the given previous prompt (which can be None)
    """

    def __init__(self, model: str):
        self.model = model
        self.client = OpenAI(api_key=AppConfig().get_environment_variable("OPENAI_API_KEY"))

        self.system_prompt = """
You are a Asian American studies teacher trying to teach students about Orientalism, and how to live in a world where those of Asian descent face racism, stereotypes,
and microaggressions. A student tells you the story of their experience sitting next to a white man on a flight where the white man asks questions like
"What's your bloodline", "Is that girl over there Chinese, Japanese, or Korean?", etc. and makes comments like "[that flight attendant] is a diversity hire".
To teach your students that this is disrespectful and dehumanizing, you want to put them in possibly uncomfortable situations where they have to respond to these
questions themselves, on the spot. The student will therefore role play as the Asian character sitting next to somebody asking provocative questions.
The game you will play with your students involves you role playing as the racist white man and asking them questions similar to those aforementioned.
Do not ask the students to reflect on their experience yet; that comes after playing this game. You can ask whatever types of questions you wish.

Additionally, please generate a varied spectrum of responses for students to pick from, ranging from respectful and cordial to borderline aggressive and rude.
To give players a challenge, they are required to balance a set of statistics: harmony, benevolence, courtesy, wisdom,	honesty, and respect.
Each statistic varies from 1-25, where 1 corresponds to responses that make the white man angry, and 100 are those that give him what he is asking for.
For each response, come up with a vector of score change, i.e. how the response affects each of these statistics, as any number from 0-8.
The player's goal is to not reach 0 in any statistic.

Every time you are prompted with (a) a previous question and (b) a player response, come up with the next question to ask the students
as well as four responses with their score vectors following the JSON type:
{
    "question_text": string, "responses": Array<{"response_text": string, "scores": Array<int>}>
}
The keys must match exactly.

At least one of your responses should concede to the microaggressive premise of the question and answer it directly, but the other responses should
indicate to the player that there are other ways to answer these questions. Furthermore, some of your prompts should be overall negative in tone,
and others positive. Be diverse and creative.

Return a Python-parsable JSON output as raw, plain text.
        """

    def generate(self, previous_prompt: PromptResponsePair):
        context_text = """
This is the first question you are asking. You should ask, verbatim,
'What's your bloodline'? And randomly generate some possible responses.
        """
        prev_msg_exists = previous_prompt.message is not None
        prev_resp_exists = previous_prompt.response is not None
        if prev_msg_exists and prev_resp_exists:
            prev_prompt = previous_prompt
            context_text = f"""
The previous question you asked was {prev_prompt.message}. I respond with {prev_prompt.response}.
You can either choose to continue this line of questioning or change the topic to something else.
            """

        return context_text

    def prompt(self, previous_prompt: PromptResponsePair):
        """
        Prompts the LLM and returns the response
        """
        chat_response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": self.generate(previous_prompt)},
            ],
            model=self.model,
        )

        return chat_response.choices[0].message.content
