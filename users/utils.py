"""
Additional utility functions that can be used in multiple locations
"""

def get_github_username(github_url):
    split_url = github_url.split('/')
    if split_url[-1] == '':
        user_name = split_url[-2]
    else:
        user_name = split_url[-1]
    return user_name