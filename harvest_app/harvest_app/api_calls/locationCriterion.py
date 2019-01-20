from googleads import adwords

def lookUpLocationsByName(service, locationNames):
    """
    Retrieves information about a location based on the 'search term'
    specified in locationNames.
    This function is hardcoded to only return postcodes.
    """
    # This time, instead of using AWQL, making a selector to retrieve.
    selector = {
        'fields': ['Id', 'LocationName', 'DisplayType', 'CanonicalName',
        'ParentLocations', 'Reach', 'TargetingStatus'],
        # Predicates are like the where of AWQL and SQL.
        'predicates': [
            {
                'field': 'LocationName',
                'operator': 'IN',
                'values': locationNames
            },
            {
                'field': 'Locale',
                'operator': 'EQUALS',
                'values': ['en']
            }
        ]
    }
    criteria = service.get(selector)
    results = []
    if not criteria:
        return 'No records were found when searching with %s.' % locationNames
    else:
        for criterion in criteria:
            # Checking wether display type is a postcode.
            if criterion['location']['displayType'] == 'Postal Code':
                # Checking wether location name is looked for.
                if criterion['location']['locationName'] in locationNames:
                    result = {'id': criterion['location']['id'],
                        'name': criterion['location']['locationName']}
                    results.append(result)
                else:
                    pass
            else:
                pass
        return results
