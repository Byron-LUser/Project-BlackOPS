names = ["bob", "jon", "Byron", "Megamind", "steve", "pet", "newman"]
new_names = []

new_names = [name for name in names if len(name) > 3]

print(new_names)