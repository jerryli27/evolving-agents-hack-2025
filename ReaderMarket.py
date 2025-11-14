
import os, sys
from genagents.genagents.genagents import GenerativeAgent
from readers_parameters import *

class ReaderMarket():
    def __init__(self):
        self.reader_agents  = []
        print('initializing reader agents...')
        for f in os.listdir(agent_bank_path):
            if len(self.reader_agents) >= num_readers:
                break
            if os.path.isdir(os.path.join(agent_bank_path, f)) :
                try:
                    agent = GenerativeAgent(agent_folder=os.path.join(agent_bank_path, f))
                    self.reader_agents.append(agent)
                    print(f"The following agent has been added as a reader: {agent.scratch}")
                except:
                    print(f"Not a valid agent path: {f}")
        print(f"{len(self.reader_agents)} reader agents have been added. ")
        print("----------")


    def get_reader_feedback(self, title: str, full_story: str, short_summary: str, timestep, price = 0.0):
        agents = self.reader_agents
        all_individual_feedback = []
        for agent in agents:
            print(f"{agent.scratch["first_name"]} {agent.scratch["last_name"]} is looking at the book {title}...")
            # First, check if the story is worth reading at all
            question = {reading_decision_prompt.format(title = title, summary = short_summary): ['yes', 'no']}
            response = agent.categorical_resp(question)
            print(f"reasoning: {response['reasonings'][0]}")
            if response['responses'][0] == 'no':
                print(f"{agent.scratch["first_name"]} {agent.scratch["last_name"]} decided to NOT to read {title}.")
                agent.remember(f"Came across a book titled {title} with the following summary: {short_summary}. Decided to not read it.", time_step=timestep)
                continue
            else:
                print(f"{agent.scratch["first_name"]} {agent.scratch["last_name"]} decided to read {title}.")
            agent.remember(f"Came across a book titled {title} with the following summary: {short_summary}. Decided to read it. The book tells the following story: {full_story}", time_step=timestep)
            
            # Ask about relevance questions
            relevance_questions = {q: [1, 10] for q in relevance_rubric}
            responses = agent.numerical_resp(relevance_questions)
            print(f"{agent.scratch["first_name"]} {agent.scratch["last_name"]} has the following thoughts in terms of the relevance of the book {title}.")
            print(responses)
            relevance_score = sum(responses["responses"]) / len(relevance_questions) / 10.0
            print(f"{agent.scratch["first_name"]} {agent.scratch["last_name"]}'s total relevance score on book {title}: {relevance_score}")
            
            # Ask about novelty questions
            expectation_questions = {q: [1, 10] for q in expectation_rubric}
            responses = agent.numerical_resp(expectation_questions)
            print(f"{agent.scratch["first_name"]} {agent.scratch["last_name"]} has the following thoughts in terms of the novelty of the book {title}.")
            print(responses)
            expectation_score = sum(responses["responses"]) / len(expectation_questions) / 10.0
            novelty_score = 1.0 - expectation_score
            print(f"{agent.scratch["first_name"]} {agent.scratch["last_name"]}'s total novelty score on book {title}: {novelty_score}")

            # Ask about quality questions
            qualty_questions = {q: [1, 10] for q in quality_rubric}
            responses = agent.numerical_resp(qualty_questions)
            print(f"{agent.scratch["first_name"]} {agent.scratch["last_name"]} has the following thoughts in terms of the quality of the book {title}.")
            print(responses)
            quality_score = sum(responses["responses"]) / len(qualty_questions) / 10.0
            print(f"{agent.scratch["first_name"]} {agent.scratch["last_name"]}'s total quality score on book {title}: {quality_score}")

            # Ask for open-ended feedback
            open_ended_response = []
            for question in open_ended_feedback:
                dialogue = [
                    ("Interviewer", question),
                ]
                
                response = agent.utterance(dialogue)
                open_ended_response.append(response)
            print(f"{agent.scratch["first_name"]} {agent.scratch["last_name"]} has the following open-ended feedback on book {title}: {'\n'.join(open_ended_response)}")
            individual_feedback = {
                'reader_agent': agent,
                'total_score' : quality_score * quality_weight + novelty_score * novelty_weight + relevance_score * relevance_weight,
                'novelty' : novelty_score,
                'relevance' : relevance_score,
                'quality' : quality_score,
                'qualitative_feedback': '\n'.join(open_ended_response)}
            
            all_individual_feedback.append(individual_feedback)
            print('-------------')
        aggregated_feedback = {
            'sold_percentage': len(all_individual_feedback) / len(agents),
            'aggregated_total_score': sum([f['total_score'] for f in all_individual_feedback]) / len(all_individual_feedback),
            'aggregated_novelty_score': sum([f['novelty'] for f in all_individual_feedback]) / len(all_individual_feedback),
            'aggregated_relevance_score': sum([f['relevance'] for f in all_individual_feedback]) / len(all_individual_feedback),
            'aggregated_quality_score': sum([f['quality'] for f in all_individual_feedback]) / len(all_individual_feedback),
            'aggregated_qualitative_feedback': "",
            'raw_feedback': all_individual_feedback
        }

        return aggregated_feedback

if __name__ == "__main__":
    # Testing with a sample story
    title = "The Awakening of Chad Everly: A Hero’s Journey Through the Algorithm"
    story_summary = """
    Chad Everly, a 25-year-old Brooklyn designer absorbed in social media and existential drift, is jolted into action when a push notification announces that his carbon footprint is “trending.” Seeking meaning, he turns to a podcaster whose pseudo-spiritual advice he mistakes for mentorship and soon plunges into the absurdities of online culture, from discourse swamps to failed influencers. Hoping to assert his significance, he launches a Substack newsletter that garners almost no real readers, then joins a desert retreat run by a startup promising to fuse blockchain and empathy, where he bonds with an AI ethics researcher named Zara. When the startup inevitably collapses, Chad loses his savings and sense of self, forcing him into a period of reflection through gardening, reading, and genuine introspection. His renewed clarity leads him to write a viral insight about the futility of optimizing life, which ironically launches him into influencer fame. In the end, he returns to the digital world as a mindful influencer, fully aware that he and those around him are still caught in an inescapable loop of curated authenticity and algorithmic performance.
    """
    full_story = """
    - Chad’s mundane life: 25-year-old freelance designer in Brooklyn, obsessed with social media, oat-milk lattes, and existential dread.
    - Inciting event: Push notification about his carbon footprint “trending” sparks a desire to make a difference.
    - Mentor appears: Listens to podcaster Eliot Vox, who gives performative, pseudo-spiritual guidance.
    - Digital trials: Faces the absurdities of online culture — the Discourse Swamp, cancelled influencers, and the Tower of the Take Economy.
    - Newsletter attempt: Launches Substack “Thoughts, Probably”, gains minimal real readership.
    - Tech-utopia retreat: Joins a desert startup retreat blending blockchain and empathy; meets AI ethics researcher Zara.
    - Romantic/spiritual bonding: Discusses crypto-spiritual philosophy, feeling enlightened and connected.
    - Collapse and crisis: Startup fails, Chad loses savings and digital identity, hits existential rock bottom.
    - Rebirth and self-discovery: Rediscovers authenticity through gardening, reading, and introspection.
    - Viral realization: Writes a viral insight about life and optimization, ironically gaining influencer fame.
    - Return to the digital world: Becomes a mindful influencer, surrounded by others chasing curated authenticity, fully aware of the algorithmic loop he can’t escape.
    """
    market = ReaderMarket()
    res = market.get_reader_feedback(title, full_story, story_summary, 1)
    print(res)
