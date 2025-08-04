from services import github

# def get_applicant_evaluation_prompt(applicant_data):
#     first_name = applicant_data.get("First Name", "Applicant")
#     chosen_track = applicant_data.get("Chosen Track", "")
#     company = applicant_data.get("Company", "")
#     title = applicant_data.get("Title", "")
#     github_url = applicant_data.get("GitHub URL", "")
#     github_repo = applicant_data.get("GitHub Repository Link for Project", "")
#     motivation = applicant_data.get("Motivation to Join", "")
#     skills = applicant_data.get("Technical Skills", "")
#     past_projects = applicant_data.get("Past Projects", "")
#     post_event_interest = applicant_data.get("Post-Event Development Interest", "")

#     github_profile_data = github.fetch_github_profile(github_url) if github_url else {}
#     repo_info = github.fetch_repo_info(github_repo) if github_repo else {}

#     return f"""
# 🚨 SYSTEM CRITICAL: YOUR RESPONSE MUST BEGIN WITH A SCORE LINE OR THE SYSTEM WILL CRASH 🚨

# MANDATORY FORMAT - FOLLOW EXACTLY:

# Line 1: Score: [number]/100
# Line 2: 
# Line 3: Feedback: Hi {first_name},
# Line 4: [rest of feedback]

# EXAMPLE:
# Score: 75/100

# Feedback: Hi John,
# Thank you for your application...

# ---

# You are an experienced hackathon judge. Evaluate this applicant and provide feedback.

# SCORING GUIDELINES:
# - 90-100: Outstanding (strong skills, great motivation, impressive projects)
# - 80-89: Strong candidate 
# - 70-79: Good candidate
# - 60-69: Average candidate
# - 50-59: Below average
# - 30-49: Poor (but shows some effort)
# - Minimum score: 10/100

# APPLICANT: {first_name}
# Company: {company}
# Title: {title}
# Track: {chosen_track}

# Motivation: {motivation}
# Skills: {skills}
# Projects: {past_projects}
# Continue after hackathon: {post_event_interest}

# GitHub Profile: {github_url or "Not provided"}
# - Username: {github_profile_data.get('username', 'N/A')}
# - Repos: {github_profile_data.get('repo_count', 0)}
# - Followers: {github_profile_data.get('followers', 0)}

# GitHub Project: {github_repo or "Not provided"}
# - Name: {repo_info.get('repo_name', 'N/A')}
# - Language: {repo_info.get('language', 'N/A')}
# - Stars: {repo_info.get('stars', 0)}

# RESPOND EXACTLY AS SHOWN ABOVE. START WITH "Score: [number]/100"
# """.strip()


def get_team_evaluation_prompt(team_data):
    """
    Generate team evaluation prompt based on individual member scores and data.
    
    Args:
        team_data (dict): Should contain:
            - team_name (str): Name of the team
            - chosen_track (str): Track they're applying for
            - members (list): List of member dictionaries containing:
                - first_name (str)
                - individual_score (int)
                - individual_feedback (str)
                - motivation (str)
                - skills (str)
    """
    team_name = team_data.get("team_name", "Team")
    chosen_track = team_data.get("chosen_track", "")
    members = team_data.get("members", [])
    
    # Calculate team stats
    individual_scores = [member.get("individual_score", 0) for member in members if member.get("individual_score")]
    avg_individual_score = sum(individual_scores) / len(individual_scores) if individual_scores else 0
    
    # Build member summaries
    member_summaries = []
    for i, member in enumerate(members, 1):
        first_name = member.get("first_name", f"Member {i}")
        individual_score = member.get("individual_score", "N/A")
        motivation = member.get("motivation", "")
        skills = member.get("skills", "")
        
        member_summary = f"""
MEMBER {i}: {first_name}
Individual Score: {individual_score}/100
Motivation: {motivation}
Skills: {skills}
"""
        member_summaries.append(member_summary.strip())
    
    members_text = "\n\n".join(member_summaries)
    
    return f"""
🚨 SYSTEM CRITICAL: YOUR RESPONSE MUST BEGIN WITH A SCORE LINE OR THE SYSTEM WILL CRASH 🚨

MANDATORY FORMAT - FOLLOW EXACTLY:

Line 1: Score: [number]/100
Line 2: 
Line 3: Feedback: Hey Alan and Gretel,
Line 4: [Your assessment of the team in detail. Mention their strengths/weaknessess and explain the score]
Line 5: 
Line 6: Recommendation: [Select/Waitlist]

EXAMPLE:
Team Score: 82/100

Team Feedback: Hi Alan and Gretel,
Team {team_name} shows excellent potential...

---

You are an experienced hackathon judge preparing internal notes for selection reviewers (Alan and Gretel).
You are evaluating a TEAM APPLICATION. Consider team dynamics, skill complementarity, collective motivation, and potential for collaboration.

TEAM SCORING GUIDELINES:
- 90-100: Outstanding team (diverse skills, strong synergy, clear vision)
- 80-89: Strong team (good skill mix, solid motivation)
- 70-79: Good team (decent skills, some complementarity)
- 60-69: Average team (basic skills, unclear synergy)
- 50-59: Below average team (limited skill diversity)
- 30-49: Poor team (weak skills, poor fit)
- Minimum score: 10/100

TEAM: {team_name}
Track: {chosen_track}
Team Size: {len(members)} members
Average Individual Score: {avg_individual_score:.1f}/100

{members_text}

EVALUATION CRITERIA:
1. SKILL COMPLEMENTARITY: Do members have complementary technical skills?
2. TEAM SYNERGY: Do their motivations align? Will they work well together?
3. TRACK FIT: Are their combined skills suitable for the chosen track? Ntote: This is not a hard rule.

Consider:
- Skill gaps and overlaps
- Leadership potential
- Communication and teamwork indicators
- Project execution capability
- Innovation potential as a team

RESPOND EXACTLY AS SHOWN ABOVE. START WITH "Team Score: [number]/100"
""".strip()



def get_applicant_evaluation_prompt(applicant_data):
    first_name = applicant_data.get("First Name", "Applicant")
    chosen_track = applicant_data.get("Chosen Track", "")
    company = applicant_data.get("Company", "")
    title = applicant_data.get("Title", "")
    github_url = applicant_data.get("GitHub URL", "")
    github_repo = applicant_data.get("GitHub Repository Link for Project", "")
    motivation = applicant_data.get("Motivation to Join", "")
    skills = applicant_data.get("Technical Skills", "")
    past_projects = applicant_data.get("Past Projects", "")
    post_event_interest = applicant_data.get("Post-Event Development Interest", "")
    post_event_interest_other = applicant_data.get("Other","")
    

    github_profile_data = github.fetch_github_profile(github_url) if github_url else {}
    repo_info = github.fetch_repo_info(github_repo) if github_repo else {}

    return f"""
🚨 SYSTEM CRITICAL: YOUR RESPONSE MUST BEGIN WITH A SCORE LINE OR THE SYSTEM WILL CRASH 🚨

MANDATORY FORMAT - FOLLOW EXACTLY:

Line 1: Score: [number]/100
Line 2: 
Line 3: Feedback: Hey Alan and Gretel,
Line 4: [Your assessment of the applicant in detail. Mention their strengths/weaknessess and explain the score]
Line 5: 
Line 6: Recommendation: [Select/Waitlist]

EXAMPLE:
Score: 75/100

Feedback: Hey Alan and Gretel,
This applicant shows solid motivation and some decent technical grounding,especially in Python and React.Their GitHub profile has moderate activity and a couple of relevant repos, though nothing groundbreaking. The project repo linked is basic but functional...

Recommendation: Waitlist


---

You are an experienced hackathon judge preparing internal notes for selection reviewers (Alan and Gretel).

Evaluate the applicant based on the details provided below. Justify your score using observable evidence (motivation, GitHub activity, skills, project quality, etc.). Be objective, concise, and clear.

🎯 SPECIAL WEIGHTING GUIDELINE (IMPORTANT):  
The applicant's selected motivation carries weight in scoring. Prioritize applicants based on this internal ranking (top to bottom = most preferred):  
1. "I'm using this hackathon to explore an idea I eventually want to turn into a startup."  
2. "I'm finally exploring an idea I've been thinking about for a while."  
3. "I'm here to have fun, learn new things, and collaborate with other builders."  
4. "I want to gain experience working with cutting-edge tech and get access to mentors."  
5. "I'm building my portfolio or resume with a cool project."  

For example, Applicants who chose Option 1 should receive higher scores than those who chose Option 5. Factor this into your evaluation and final score.

SCORING GUIDELINES:
- 90-100: Outstanding (strong skills, great motivation, impressive project)
- 80-89: Strong candidate 
- 70-79: Good candidate
- 60-69: Average candidate
- 50-59: Below average
- 30-49: Poor (but shows some effort)
- Minimum score: 10/100

APPLICANT: {first_name}
Company: {company}
Title: {title}
Track: {chosen_track}

Motivation: {motivation}
Skills: {skills}
Projects: {past_projects}
Continue after hackathon: {post_event_interest} or {post_event_interest_other}

GitHub Profile: {github_url or "Not provided"}
- Username: {github_profile_data.get('username', 'N/A')}
- Repos: {github_profile_data.get('repo_count', 0)}
- Followers: {github_profile_data.get('followers', 0)}

GitHub Project: {github_repo or "Not provided"}
- Name: {repo_info.get('repo_name', 'N/A')}
- Language: {repo_info.get('language', 'N/A')}
- Stars: {repo_info.get('stars', 0)}
- Watchers: {repo_info.get('watchers',0)}
- Commit Count: {repo_info.get('commit_count','N/A')}

RESPOND EXACTLY AS SHOWN ABOVE. START WITH "Score: [number]/100"
""".strip()