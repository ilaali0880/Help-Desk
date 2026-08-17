
def is_agent(user):
    return user.groups.filter(name='Agents').exists()