from collections import defaultdict
from pyairtable import Api
from config import settings

API_KEY = settings.AIRTABLE_API_KEY
BASE_ID = settings.AIRTABLE_BASE_ID
TABLE_NAME = settings.AIRTABLE_TABLE_NAME

FIELDS_TO_FETCH = [
    "Chosen Track", "First Name", "Last Name", "Company", "Title",
    "GitHub URL", "Motivation to Join", "Technical Skills", "Past Projects",
    "GitHub Repository", "Post-Event Development Interest", "Other"
]

def test_read_airtable():
    try:
        api = Api(API_KEY)
        table = api.table(BASE_ID, TABLE_NAME)
        records = table.all()
        print(f"Fetched {len(records)} records from Airtable:")
        for rec in records:
            print(rec['fields'])
    except Exception as e:
        print(f"Error reading from Airtable: {e}")

def fetch_applicants_for_evaluation():
    api = Api(API_KEY)
    table = api.table(BASE_ID, TABLE_NAME)
    records = table.all()
    applicants = []
    for rec in records:
        fields = rec.get("fields", {})
        applicant = {field: fields.get(field, "") for field in FIELDS_TO_FETCH}
        applicant["record_id"] = rec["id"]  # for updating back later
        applicants.append(applicant)
    return applicants

# Fields needed for team evaluation
TEAM_FIELDS_TO_FETCH = [
    "First Name", 
    "Team Code", 
    "Team Name",
    "Chosen Track",
    "Individual Score", 
    "Individual Feedback",
    "Motivation to Join", 
    "Technical Skills"
    
]

def fetch_applicants_for_team_evaluation():
    """
    Fetch all applicants that have team codes for team evaluation.
    """
    api = Api(API_KEY)
    table = api.table(BASE_ID, TABLE_NAME)
    records = table.all()
    
    applicants = []
    for rec in records:
        fields = rec.get("fields", {})
        # Only include applicants that have a team code
        if fields.get("Team Code"):
            applicant = {field: fields.get(field, "") for field in TEAM_FIELDS_TO_FETCH}
            applicant["record_id"] = rec["id"]  # for updating back later
            applicants.append(applicant)
    
    return applicants

def group_applicants_by_team(applicants):
    """
    Group applicants by their team code.
    Returns a dictionary where keys are team codes and values are lists of applicants.
    """
    teams = defaultdict(list)
    
    for applicant in applicants:
        team_code = applicant.get("Team Code", "").strip()
        if team_code:  # Only add if team code exists and is not empty
            teams[team_code].append(applicant)
    
    # Filter out teams with only 1 member (they might be individual applicants or nobody joined their team)
    return {team_code: members for team_code, members in teams.items() if len(members) > 1}

def prepare_team_data_for_ai(team_code, team_members):
    """
    Prepare team data in the format expected by get_team_evaluation_prompt().
    """
    if not team_members:
        return None
    
    # Use the chosen track from the first member (assuming all team members have same track)
    chosen_track = team_members[0].get("Chosen Track", "")
    
    # Prepare member data
    members = []
    for member in team_members:
        member_data = {
            "first_name": member.get("First Name", ""),
            "individual_score": member.get("Individual Score", 0),
            "individual_feedback": member.get("Individual Feedback", ""),
            "motivation": member.get("Motivation to Join", ""),
            "skills": member.get("Technical Skills", "")
        }
        members.append(member_data)
        
    team_name = team_members[0].get("Team Name", f"Team {team_code}")  # fallback to code
    
    team_data = {
        "team_name": team_name,
        "chosen_track": chosen_track,
        "members": members
    }
    
    return team_data

def update_team_members_in_airtable(team_members, team_score, team_feedback):
    """
    Update all team members with the same team score and team feedback.
    """
    api = Api(API_KEY)
    table = api.table(BASE_ID, TABLE_NAME)
    
    for member in team_members:
        try:
            table.update(member["record_id"], {
                "Team Score": team_score if team_score is not None else 0,
                "Team Feedback": team_feedback if team_feedback else "No team feedback generated."
            })
            print(f"Updated team member {member.get('First Name')} with team score {team_score}")
        except Exception as e:
            print(f"Error updating team member {member.get('First Name')}: {e}")