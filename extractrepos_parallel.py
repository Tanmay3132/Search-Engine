from github import Github

def extract_repos(userquery, repos_results, count=20):
    g = Github()
    
    repositories = g.search_repositories(query=userquery)
    for i in range(count):
        repos_results.append(tuple(['https://github.com/'+ repositories[i].full_name, repositories[i].stargazers_count]))