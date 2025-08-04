import requests
import base64
from urllib.parse import urlparse

def fetch_repo_info(repo_url, include_readme=True):
    """
    Fetch public GitHub project repo info via API:
    - stars, forks, watchers, language, last commit date, README content
    
    Args:
        repo_url (str): GitHub repository URL
        include_readme (bool): Whether to fetch README content
    """
    if not repo_url or not repo_url.strip():
        return {
            "repo_name": "",
            "stars": 0,
            "forks": 0,
            "watchers": 0,
            "language": "",
            "last_commit_date": None,
            "readme_content": None,
            "readme_filename": None
        }
    
    try:
        # More robust URL parsing
        url = repo_url.strip().rstrip('/')
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        parsed = urlparse(url)
        path_parts = parsed.path.strip('/').split('/')
        
        if len(path_parts) < 2 or parsed.netloc != 'github.com':
            return {"error": "Invalid GitHub repo URL"}

        owner, repo = path_parts[0], path_parts[1]
        # Remove .git suffix if present
        if repo.endswith('.git'):
            repo = repo[:-4]
            
        repo_api_url = f"https://api.github.com/repos/{owner}/{repo}"
        
        # Add headers for better rate limiting
        headers = {'Accept': 'application/vnd.github.v3+json'}
        
        repo_resp = requests.get(repo_api_url, headers=headers)
        
        if repo_resp.status_code != 200:
            return {"error": f"Repo API returned status {repo_resp.status_code}"}

        repo_data = repo_resp.json()
        
        # Build base response
        result = {
            "repo_name": repo_data.get("name"),
            "stars": repo_data.get("stargazers_count", 0),
            "forks": repo_data.get("forks_count", 0),
            "watchers": repo_data.get("watchers_count", 0),
            "language": repo_data.get("language", ""),
            "last_commit_date": repo_data.get('pushed_at'),
            "readme_content": None,
            "readme_filename": None
        }
        
        # Fetch README if requested
        if include_readme:
            readme_info = fetch_readme(owner, repo, headers)
            result.update(readme_info)
        
        return result

    except Exception as e:
        return {"error": str(e)}


def fetch_readme(owner, repo, headers):
    """
    Fetch README content from a GitHub repository using the direct README endpoint.
    """
    try:
        # Direct README endpoint - GitHub automatically finds the README file
        readme_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
        readme_resp = requests.get(readme_url, headers=headers)
        
        if readme_resp.status_code == 200:
            readme_data = readme_resp.json()
            
            # README content is base64 encoded
            if readme_data.get('content'):
                content = base64.b64decode(readme_data['content']).decode('utf-8')
                return {
                    "readme_content": content,
                    "readme_filename": readme_data.get('name', 'README')
                }
                
    except Exception:
        pass
    
    # No README found or error occurred
    return {
        "readme_content": None,
        "readme_filename": None
    }


def fetch_readme_only(repo_url):
    """
    Convenience function to fetch only README content
    """
    result = fetch_repo_info(repo_url, include_readme=True)
    
    if "error" in result:
        return result
    
    return {
        "readme_content": result.get("readme_content"),
        "readme_filename": result.get("readme_filename")
    }


# Example usage:
if __name__ == "__main__":
    # Test with a popular repo
    repo_info = fetch_repo_info("https://github.com/sammchardy/python-binance")
    
    if "error" not in repo_info:
        print(f"Repo: {repo_info['repo_name']}")
        print(f"Stars: {repo_info['stars']}")
        print(f"Language: {repo_info['language']}")
        print(f"README file: {repo_info['readme_filename']}")
        
    if repo_info['readme_content']:
        lines = repo_info['readme_content'].split('\n')
        print("README (first 30 lines):")
        print('\n'.join(lines[:10]))
        

    else:
        print(f"Error: {repo_info['error']}")