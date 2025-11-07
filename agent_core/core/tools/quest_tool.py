from langchain.tools import tool
from agent_core.core.prompts.questPromptTemplate import prompt
import json

def get_quest_tool(llm):
    @tool
    def generate_dynamic_quest(chapter_id:int, player_state:dict) ->str:
        """
        Given a chapter of the main story and current player state,
        generate a dynamic quest objective that fits within the story boundaries.
        """
        story = json.load(open("agent_core/story/main_storyline.json"))
        chapter = next(c for c in story["chapters"] if c["id"] == chapter_id)
        
        messages = prompt.format_messages(
            chapter=chapter, player_state=player_state
        )

        response = llm.invoke(messages)
        return getattr(response, "content", str(response))
   
    return generate_dynamic_quest