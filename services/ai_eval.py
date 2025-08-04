# from openai import OpenAI
# from config.settings import OPENAI_API_KEY
# from prompts.prompts_template import get_applicant_evaluation_prompt

# client = OpenAI(api_key=OPENAI_API_KEY)


from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from config.settings import CLAUDE_API_KEY
from prompts.prompts_template import get_applicant_evaluation_prompt

client = Anthropic(api_key=CLAUDE_API_KEY)

def evaluate_applicant(applicant_data):
    prompt = get_applicant_evaluation_prompt(applicant_data)

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


import re

def parse_ai_response(response_text):
    """
    Simple parser for AI evaluation responses.
    Extracts score and feedback without making assumptions about quality.
    """
    score = None
    
    # Look for score patterns in order of preference
    score_patterns = [
        r'Score:\s*(\d+)/100',           # "Score: 85/100"
        r'Score:\s*(\d+)',               # "Score: 85"
        r'(\d+)/100',                    # "85/100"
        r'(\d+)\s*out of 100',           # "85 out of 100"
        r'(\d+)\s*points',               # "85 points"
        r'(\d+)\s*%',                    # "85%"
    ]
    
    for pattern in score_patterns:
        match = re.search(pattern, response_text, re.IGNORECASE)
        if match:
            try:
                extracted_score = int(match.group(1))
                # Only validate it's a reasonable number (0-100)
                if 0 <= extracted_score <= 100:
                    score = extracted_score
                    break
            except (ValueError, IndexError):
                continue
    
    # Extract feedback
    feedback_match = re.search(r'Feedback:\s*(.*)', response_text, re.DOTALL | re.IGNORECASE)
    if feedback_match:
        feedback = feedback_match.group(1).strip()
    else:
        # If no "Feedback:" found, use the entire response minus the score line
        feedback_lines = []
        for line in response_text.split('\n'):
            if not re.match(r'Score:\s*\d+', line, re.IGNORECASE):
                feedback_lines.append(line)
        feedback = '\n'.join(feedback_lines).strip()
    
    # If no score found, return None and let the caller decide what to do
    if score is None:
        print(f"Warning: Could not extract score from response")
        score=10
        feedback = response_text.strip()
    
    return score, feedback


def evaluate_team(team_data):
    """
    Evaluate a team using AI and return the response.
    """
    from anthropic import Anthropic
    from config.settings import CLAUDE_API_KEY
    from prompts.prompts_template import get_team_evaluation_prompt
    
    client = Anthropic(api_key=CLAUDE_API_KEY)
    prompt = get_team_evaluation_prompt(team_data)

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


def parse_team_ai_response(response_text):
    """
    Parse AI response to extract team score and team feedback.
    Similar to parse_ai_response but for team evaluation.
    """
    import re
    
    score = None
    
    # Look for team score patterns in order of preference
    score_patterns = [
        r'Team Score:\s*(\d+)/100',      # "Team Score: 85/100"
        r'Team Score:\s*(\d+)',          # "Team Score: 85"
        r'Score:\s*(\d+)/100',           # "Score: 85/100" (fallback)
        r'Score:\s*(\d+)',               # "Score: 85" (fallback)
        r'(\d+)/100',                    # "85/100"
        r'(\d+)\s*out of 100',           # "85 out of 100"
        r'(\d+)\s*points',               # "85 points"
        r'(\d+)\s*%',                    # "85%"
    ]
    
    for pattern in score_patterns:
        match = re.search(pattern, response_text, re.IGNORECASE)
        if match:
            try:
                extracted_score = int(match.group(1))
                # Only validate it's a reasonable number (0-100)
                if 0 <= extracted_score <= 100:
                    score = extracted_score
                    break
            except (ValueError, IndexError):
                continue
    
    # Extract team feedback
    feedback_match = re.search(r'Team Feedback:\s*(.*)', response_text, re.DOTALL | re.IGNORECASE)
    if feedback_match:
        feedback = feedback_match.group(1).strip()
    else:
        # Fallback to regular "Feedback:" pattern
        feedback_match = re.search(r'Feedback:\s*(.*)', response_text, re.DOTALL | re.IGNORECASE)
        if feedback_match:
            feedback = feedback_match.group(1).strip()
        else:
            # If no "Feedback:" found, use the entire response minus the score line
            feedback_lines = []
            for line in response_text.split('\n'):
                if not re.match(r'(Team\s+)?Score:\s*\d+', line, re.IGNORECASE):
                    feedback_lines.append(line)
            feedback = '\n'.join(feedback_lines).strip()
    
    # If no score found, return default score and let caller decide what to do
    if score is None:
        print(f"Warning: Could not extract team score from response")
        score = 10
        feedback = response_text.strip()
    
    return score, feedback