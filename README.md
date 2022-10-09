# tcg-collection-tools
A tool for helping you to keep track of your TCG (Trading Card Game) collection
Uses the [Scryfall](https://scryfall.com/docs/api) api to get card information for MTG, although you can also download the [bulkdata](https://scryfall.com/docs/api/bulk-data) yourself and point to that at startup
# Necessary vars
- os.environ['DJANGO_SECRET']
- os.environ['UPDATE_FROM_API'] = 'False'
    - Dictates whether db data will be updated from the api or a file
    - Either 'True' or 'False'
- os.environ['MTG_FILE_LOCATION'] = 'C:\\Users\\edeno\\Downloads\\default-cards-20220927090638.json'
    - Location to read data for the game MTG from
- os.environ['MTG_UPDATE'] = 'False'
    -   Dictates whether MTG related tables should be updated
    - Either 'True' or 'False'
- os.environ['DEBUG'] = 'True'
    - Either 'True' or 'False'
