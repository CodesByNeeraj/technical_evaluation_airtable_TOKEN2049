from pyairtable import Table
from config.settings import AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME,OPENAI_API_KEY,CLAUDE_API_KEY
from services.ai_eval import evaluate_applicant, parse_ai_response
from services.airtable import fetch_applicants_for_evaluation
from services.ai_eval import evaluate_team, parse_team_ai_response
from services.airtable import fetch_applicants_for_team_evaluation, group_applicants_by_team, prepare_team_data_for_ai, update_team_members_in_airtable

table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)

def run_evaluation_and_update():
    applicants = fetch_applicants_for_evaluation()
    for applicant in applicants:
        try:
            ai_output = evaluate_applicant(applicant)
            score, feedback = parse_ai_response(ai_output)

            if score is None:
                print(f"Warning: No score parsed for applicant {applicant.get('First Name')}")

            # Update Airtable record with Score and Feedback
            table.update(applicant["record_id"], {
                "Individual Score": score if score is not None else 0,
                "Individual Feedback": feedback if feedback else "No feedback generated."
            })
            print(f"Updated applicant {applicant.get('First Name')} with score {score}")
        except Exception as e:
            print(f"Error evaluating applicant {applicant.get('First Name')}: {e}")
            

def run_team_evaluation_and_update():
    """
    Main function to run team evaluation pipeline.
    """
    # Step 1: Fetch all applicants with team codes
    print("Fetching applicants for team evaluation...")
    applicants = fetch_applicants_for_team_evaluation()
    print(f"Found {len(applicants)} applicants with team codes")
    
    # Step 2: Group by team code
    print("Grouping applicants by team...")
    teams = group_applicants_by_team(applicants)
    print(f"Found {len(teams)} teams to evaluate")
    
    # Step 3: Evaluate each team
    for team_code, team_members in teams.items():
        print(f"\n--- Evaluating Team {team_code} ({len(team_members)} members) ---")
        
        try:
            # Prepare team data
            team_data = prepare_team_data_for_ai(team_code, team_members)
            
            if not team_data:
                print(f"Warning: Could not prepare data for team {team_code}")
                continue
            
            # Get AI evaluation
            ai_output = evaluate_team(team_data)
            
            # Parse response
            team_score, team_feedback = parse_team_ai_response(ai_output)
            
            if team_score is None:
                print(f"Warning: No team score parsed for team {team_code}")
            
            # Update all team members in Airtable
            update_team_members_in_airtable(team_members, team_score, team_feedback)
            
            print(f"Successfully evaluated team {team_code} with score {team_score}")
            
        except Exception as e:
            print(f"Error evaluating team {team_code}: {e}")
            # Continue with next team even if this one fails
            
            
if __name__ == "__main__":
    #run_evaluation_and_update()
    run_team_evaluation_and_update()
