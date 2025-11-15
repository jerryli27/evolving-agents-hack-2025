
import os, sys
from genagents.genagents.genagents import GenerativeAgent
from readers_parameters import *
from genagents.simulation_engine.settings import OPENAI_API_KEY, LLM_VERS
import re
import json

import openai

def query_gpt(prompt, model=LLM_VERS, temperature=0.01):
    openai.api_key = OPENAI_API_KEY
    #print(f"querying gpt... the prompt is: {prompt}")
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content
    except openai.AuthenticationError:
        return "Error: Invalid API key. Please check your readers_parameters.py file."
    except openai.RateLimitError:
        return "Error: Rate limit exceeded. Please wait before making another request."
    except Exception as e:
        return f"Error: {str(e)}"

def extract_integer(text):
    # Look for an integer (including negative numbers)
    match = re.search(r'-?\d+', text)
    if match:
        return int(match.group())
    return None


class ReaderMarket():
    def __init__(self):
        self.reader_agents  = []
        self.agent_prediction = {}
        print('initializing reader agents...')
        for f in os.listdir(agent_bank_path):
            if len(self.reader_agents) >= num_readers:
                break
            if os.path.isdir(os.path.join(agent_bank_path, f)) :
                try:
                    agent = GenerativeAgent(agent_folder=os.path.join(agent_bank_path, f))
                    self.reader_agents.append(agent)
                    self.agent_prediction[agent.scratch['first_name'] + ' ' + agent.scratch['last_name']] = ''
                    print(f"The following agent has been added as a reader: {agent.scratch}")
                except:
                    print(f"Not a valid agent path: {f}")
        print(f"{len(self.reader_agents)} reader agents have been added. ")
        print("----------")

    def get_reader_feedback(self, title: str,
        full_story_summary: str,
        episode_story: str,
        episode_summary: str,
        timestep: int, price = 0.0):
        agents = self.reader_agents
        all_individual_feedback = []
        for agent in agents:
            print(f"{agent.scratch["first_name"]} {agent.scratch["last_name"]} is scrolling through episode {timestep} of the short drama series {title}...")
            # First, check if the story is worth reading at all
            #question = {reading_decision_prompt.format(title = title, full_story_summary = full_story_summary, summary = episode_summary, timestep = timestep): ['yes', 'no']}
            #response = agent.categorical_resp(question)
            #print(f"reasoning: {response['reasonings'][0]}")
            #if response['responses'][0] == 'no':
            #    print(f"{agent.scratch["first_name"]} {agent.scratch["last_name"]} decided to NOT to watch episode {timestep} of {title}.")
            #    agent.remember(f"Came across a short drama series titled {title} with the following summary of episode {timestep}: {episode_summary}. Decided to not watch it.", time_step=timestep)
            #    continue
            #else:
            print(f"{agent.scratch["first_name"]} {agent.scratch["last_name"]} decided to watch episode {timestep} of {title}.")
            agent.remember(f"Came across a short drama series titled {title} with the following summary of episode {timestep}: {episode_summary}. Decided to watch it. The episode presents the following plot: {episode_story}", time_step=timestep)
            
            # Ask about relevance questions
            relevance_questions = {q: [1, 10] for q in relevance_rubric}
            responses = agent.numerical_resp(relevance_questions)
            print(f"{agent.scratch["first_name"]} {agent.scratch["last_name"]} has the following thoughts in terms of the relevance of the show {title}.")
            print(responses)
            relevance_score = sum(responses["responses"]) / len(relevance_questions) / 10.0
            print(f"{agent.scratch["first_name"]} {agent.scratch["last_name"]}'s total relevance score on show {title}: {relevance_score}")
            
            # Ask about novelty questions
            prediction = self.agent_prediction[agent.scratch['first_name'] + ' ' + agent.scratch['last_name']] if timestep > 1 else ""
            expectation_questions = {q: [1, 10] for q in expectation_rubric}
            # Compare agent's prediction with the actual episode content
            similarity = None
            if timestep > 1:
                print(f"{agent.scratch["first_name"]} {agent.scratch["last_name"]} has the following prediction of what this episode will be like: {prediction}")
                try:
                    response = query_gpt(prediction_alignment_prompt.format(actual_story = episode_story, prediction = prediction))
                    print('response:', response)
                    similarity = extract_integer(response)
                except Exception as e:
                    print(e)
                    print('Failed in getting alignment score.')

            expectation_questions = {q: [1, 10] for q in expectation_rubric}
            # Compare agent's prediction with the actual episode content
            similarity = None
            if timestep > 1:
                print(f"{agent.scratch["first_name"]} {agent.scratch["last_name"]} has the following prediction of what this episode will be like: {prediction}")
                try:
                    response = query_gpt(prediction_alignment_prompt.format(actual_story = episode_story, prediction = prediction))
                    print('response:', response)
                    similarity = extract_integer(response)
                except Exception as e:
                    print(e)
                    print('Failed in getting alignment score.')

            responses = agent.numerical_resp(expectation_questions)
            if similarity != None:
                responses['responses'][0] = similarity

            print(f"{agent.scratch["first_name"]} {agent.scratch["last_name"]} has the following thoughts in terms of the novelty of the show {title}.")
            print(responses)
            expectation_score = sum(responses["responses"]) / len(expectation_questions) / 10.0
            novelty_score = 1.0 - expectation_score
            print(f"{agent.scratch["first_name"]} {agent.scratch["last_name"]}'s total novelty score on show {title}: {novelty_score}")

            # Ask about quality questions
            qualty_questions = {q: [1, 10] for q in quality_rubric}
            responses = agent.numerical_resp(qualty_questions)
            print(f"{agent.scratch["first_name"]} {agent.scratch["last_name"]} has the following thoughts in terms of the quality of the show {title}.")
            print(responses)
            quality_score = sum(responses["responses"]) / len(qualty_questions) / 10.0
            print(f"{agent.scratch["first_name"]} {agent.scratch["last_name"]}'s total quality score on show {title}: {quality_score}")

            # Ask for open-ended feedback
            open_ended_response = []
            for question in open_ended_feedback:
                dialogue = [
                    ("Interviewer", question),
                ]
                
                response = agent.utterance(dialogue)
                open_ended_response.append(response)
            print(f"{agent.scratch["first_name"]} {agent.scratch["last_name"]} has the following open-ended feedback on show {title}: {'\n'.join(open_ended_response)}")

            # Predict next episode
            dialogue = [
                    ("Interviewer", plot_prediction_prompt),
                ]
            prediction = agent.utterance(dialogue)
            self.agent_prediction[agent.scratch['first_name'] + ' ' + agent.scratch['last_name']] = f"{prediction}"

            individual_feedback = {
                "reader_agent": f"{agent.scratch['first_name']} {agent.scratch['last_name']}",
                "total_score" : quality_score * quality_weight + novelty_score * novelty_weight + relevance_score * relevance_weight,
                "novelty" : novelty_score,
                "relevance" : relevance_score,
                "quality" : quality_score,
                "qualitative_feedback": '\n'.join(open_ended_response),
                "prediction_for_next_episode": prediction}
            
            all_individual_feedback.append(individual_feedback)
            print('-------------')
        aggregated_feedback = {
            "sold_percentage": len(all_individual_feedback) / len(agents),
            "aggregated_total_score": 0. if len(all_individual_feedback) == 0 else sum([f['total_score'] for f in all_individual_feedback]) / len(all_individual_feedback),
            "aggregated_novelty_score": 0. if len(all_individual_feedback) == 0 else sum([f['novelty'] for f in all_individual_feedback]) / len(all_individual_feedback),
            "aggregated_relevance_score": 0. if len(all_individual_feedback) == 0 else sum([f['relevance'] for f in all_individual_feedback]) / len(all_individual_feedback),
            "aggregated_quality_score": 0. if len(all_individual_feedback) == 0 else sum([f['quality'] for f in all_individual_feedback]) / len(all_individual_feedback),
            "aggregated_qualitative_feedback": query_gpt(qualitative_feedback_aggregation_prompt.format(all_feedback = '\n'.join([f"Feedback from {f['reader_agent']}: {f['qualitative_feedback']}" for f in all_individual_feedback]))),
            "aggregated_prediction_for_next_episode": query_gpt(prediction_aggregation_prompt.format(all_prediction = '\n'.join([f"Prediction from {f['reader_agent']}: {f['prediction_for_next_episode']}" for f in all_individual_feedback]))),
            "raw_feedback": all_individual_feedback
        }

        return aggregated_feedback

if __name__ == "__main__":
    #print(query_gpt('when is Meiji restoration?'))
    # Testing with a sample story
    #title = "The Awakening of Chad Everly: A Hero’s Journey Through the Algorithm"
    #story_summary = """
    #Chad Everly, a 25-year-old Brooklyn designer absorbed in social media and existential drift, is jolted into action when a push notification announces that his carbon footprint is “trending.” Seeking meaning, he turns to a podcaster whose pseudo-spiritual advice he mistakes for mentorship and soon plunges into the absurdities of online culture, from discourse swamps to failed influencers. Hoping to assert his significance, he launches a Substack newsletter that garners almost no real readers, then joins a desert retreat run by a startup promising to fuse blockchain and empathy, where he bonds with an AI ethics researcher named Zara. When the startup inevitably collapses, Chad loses his savings and sense of self, forcing him into a period of reflection through gardening, reading, and genuine introspection. His renewed clarity leads him to write a viral insight about the futility of optimizing life, which ironically launches him into influencer fame. In the end, he returns to the digital world as a mindful influencer, fully aware that he and those around him are still caught in an inescapable loop of curated authenticity and algorithmic performance.
    #"""
    #episode_story = """
    #- Chad’s mundane life: 25-year-old freelance designer in Brooklyn, obsessed with social media, oat-milk lattes, and existential dread.
    #- Inciting event: Push notification about his carbon footprint “trending” sparks a desire to make a difference.
    #- Mentor appears: Listens to podcaster Eliot Vox, who gives performative, pseudo-spiritual guidance.
    #- Digital trials: Faces the absurdities of online culture — the Discourse Swamp, cancelled influencers, and the Tower of the Take Economy.
    #- Newsletter attempt: Launches Substack “Thoughts, Probably”, gains minimal real readership.
    #- Tech-utopia retreat: Joins a desert startup retreat blending blockchain and empathy; meets AI ethics researcher Zara.
    #- Romantic/spiritual bonding: Discusses crypto-spiritual philosophy, feeling enlightened and connected.
    #- Collapse and crisis: Startup fails, Chad loses savings and digital identity, hits existential rock bottom.
    #- Rebirth and self-discovery: Rediscovers authenticity through gardening, reading, and introspection.
    #- Viral realization: Writes a viral insight about life and optimization, ironically gaining influencer fame.
    #- Return to the digital world: Becomes a mindful influencer, surrounded by others chasing curated authenticity, fully aware of the algorithmic loop he can’t escape.
    #"""

    title = "The Cartographer's Daughter"
    story_summary = """
    "A young woman in 1943 Berlin must choose between family loyalty and moral conscience when she discovers her father's maps are being used to target Jewish neighborhoods for deportation."
    """
    episode_summaries = [
        "Berlin, March 1943. Amid Allied bombing raids, Greta Hoffman navigates life in a city under siege. She admires her father Heinrich, Berlin’s most respected cartographer, and takes pride in his work, unaware of the dark purpose it serves.",
        "Greta discovers a stack of her father’s maps in a Gestapo officer’s briefcase, marked with red circles and coded numbers. Horrified, she realizes the maps are being used to identify and deport Jewish families. Confronting her father, she learns of the impossible choice he faces: comply with the Gestapo or risk the death of his family.",
        "Torn between love for her father and moral outrage, Greta wrestles with her conscience. She considers sabotaging the maps to save lives but fears the consequences for her family. The chapter explores her internal conflict and the impossible moral choices faced under totalitarian rule.",
        "Greta devises a careful plan to alter the maps, misdirecting the Gestapo while minimizing risk to her father. Working under pressure, she executes the sabotage with precision, demonstrating courage, ingenuity, and moral resolve.",
        "The sabotage is discovered, forcing Greta to flee into the very neighborhoods her father once mapped. She finds refuge among the people she tried to save, confronting the dangers and complexities of survival. A final confrontation with her father underscores the story’s moral tension and the personal cost of conscience.",
        "Greta reflects on complicity, resistance, and the sacrifices required to protect loved ones. The story closes by highlighting the courage it takes to act with conscience under tyranny and the blurred lines between right and wrong in times of unimaginable pressure."
    ]

    episode_stories = [
        "Berlin, March 1943. Amid Allied bombing raids, Greta Hoffman navigates life in a city under siege. She admires her father Heinrich, Berlin’s most respected cartographer, and takes pride in his work, unaware of the dark purpose it serves.",
        "Greta discovers a stack of her father’s maps in a Gestapo officer’s briefcase, marked with red circles and coded numbers. Horrified, she realizes the maps are being used to identify and deport Jewish families. Confronting her father, she learns of the impossible choice he faces: comply with the Gestapo or risk the death of his family.",
        "Torn between love for her father and moral outrage, Greta wrestles with her conscience. She considers sabotaging the maps to save lives but fears the consequences for her family. The chapter explores her internal conflict and the impossible moral choices faced under totalitarian rule.",
        "Greta devises a careful plan to alter the maps, misdirecting the Gestapo while minimizing risk to her father. Working under pressure, she executes the sabotage with precision, demonstrating courage, ingenuity, and moral resolve.",
        "The sabotage is discovered, forcing Greta to flee into the very neighborhoods her father once mapped. She finds refuge among the people she tried to save, confronting the dangers and complexities of survival. A final confrontation with her father underscores the story’s moral tension and the personal cost of conscience.",
        "Greta reflects on complicity, resistance, and the sacrifices required to protect loved ones. The story closes by highlighting the courage it takes to act with conscience under tyranny and the blurred lines between right and wrong in times of unimaginable pressure."
    ]

    market = ReaderMarket()
    for i in range(6):
        print(f"--- Episode {i+1} ---")
        res = market.get_reader_feedback(title, story_summary, episode_stories[i], episode_summaries[i], i+1)
        print(json.dumps(res, indent=4))