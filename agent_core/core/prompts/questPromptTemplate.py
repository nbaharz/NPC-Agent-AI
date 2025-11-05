from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert narrative designer AI that creates coherent side quests."),
    ("human", """
    Main story context:
    {chapter}

    Player current state:
    {player_state}

    Generate a unique side quest that helps the player advance toward the main goal,
    but stays logically consistent with the main story.
    The quest should have:
    - title
    - description
    - objective
    - possible outcomes
    """)
])
