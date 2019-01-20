from googleads import adwords

pageSize = 100

"""
Make sure to have a MCC account id as the client_customer_id in the googleads.yaml file.
Having any other account id can result in weird and unwanted behaviour.
DO THIS AT YOUR OWN RISK!
"""

def getAllAccounts(service):
    """
    Retrieve all accounts under a manager account (MCC).
    """
    offset = 0
    # Creating the selector
    selector = {
        'fields': ['CustomerId', 'Name'],
        'paging': {
            'startIndex': str(offset),
            'numberResults': str(pageSize)
        }
    }
    accounts= []
    morePages = True
    try:
        while morePages:
            # Calling the API to retrieve data based on selector.
            page = service.get(selector)
            if 'entries' in page:
                for account in page['entries']:
                    accounts.append(account)
            else:
                pass
            offset += pageSize
            selector['paging']['startIndex'] = str(offset)
            morePages = offset < int(page['totalNumEntries'])
        return accounts
    # TODO: Catch specific exception.
    except Exception as e:
        print('exception:\n\t', e, '\n')
        return ('No client account found with ID ')
