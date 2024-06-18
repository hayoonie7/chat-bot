import league

def handle_response(message):
    if message == None: return
    lower_message = message.lower()
    if lower_message == "hello":
        return "Hi there!"
    elif message.startswith("/id:"):
        given_id = message.split(":")[1]
        name = given_id.split("#")[0]
        tagline = given_id.split("#")[1]
        print(f'Name: {name}, Tagline: {tagline}')
        return league.get_summoner(name, tagline)
    elif lower_message == "goodbye":
        return "See you later!"

