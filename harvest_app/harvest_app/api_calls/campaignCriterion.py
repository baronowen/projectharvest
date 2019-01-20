from googleads import adwords

pageSize = 500

def getCriteriaWithBid(service, campaignId):
    """
    Retrieves all targeting criteria for a given campaign.

    This function returns a dictionary with the name and bid modifier.
    """
    offset = 0
    selector = {
        'fields': ['CampaignId', 'Id', 'CriteriaType', 'LocationName',
            'BidModifier', 'CampaignCriterionStatus', 'BaseCampaignId'],
        # Predicates acts like the where part of SQL and AWQL.
        'predicates': [
            {
                'field': 'CampaignId',
                'operator': 'EQUALS',
                'values': [campaignId]
            },
            {
                'field': 'CriteriaType',
                'operator': 'EQUALS',
                'values': ['LOCATION']
            },
        ],
        'paging': {
            'startIndex': str(offset),
            'numberResults': str(pageSize)
        }
    }

    results = []
    morePages = True
    while morePages:
        # Calling API
        page = service.get(selector)

        if 'entries' in page:
            for criterion in page['entries']:
                displayType = criterion['criterion']['displayType']
                if displayType == 'Postal Code':
                    # Adding a dictionary with location name and bid modifier
                    # to the list that is returned.
                    results.append({'name': criterion['criterion']['locationName'],
                        'bidMod': criterion['bidModifier']})
                else:
                    pass
        else:
            pass
        offset += pageSize
        selector['paging']['startIndex'] = str(offset)
        morePages = offset < int(page['totalNumEntries'])
    return results

def addCriteria(service, campaignId, locIds, targetList, bidModifier, returnOp=False, doChecks=True):
    """
    Add a location criteria to a campaign.
    Requires the ID of a location you wish to add.
    """
    locList = []
    operations = []
    bidModifier = float(bidModifier)
    if doChecks:
        for id in locIds:
            if isinstance(id, str):
                pass
            else:
                if id['name'] in targetList:
                    pass
                else:
                    locList.append({
                        'xsi_type': 'Location',
                        # ID is found by using lookUpLocationsByName in
                        # locationCriterion
                        'id': id['id']
                    })
    else:
        for id in locIds:
            locList.append({
                'xsi_type': 'Location',
                'id': id['id']
            })
    # Checking wether there are locations to add.
    if not locList:
        return('No new location(s) to target or given location(s) do not exist.')
    else:
        if bidModifier == 0:
            for criterion in locList:
                # Creating operations list.
                operations.append({
                    'operator': 'ADD',
                    'operand': {
                        'campaignId': campaignId,
                        # Criterion contains the id of the location to target.
                        'criterion': criterion
                    }
                })
        else:
            for criterion in locList:
                operations.append({
                    'operator': 'ADD',
                    'operand': {
                        'campaignId': campaignId,
                        'criterion': criterion,
                        'bidModifier': bidModifier
                    }
                })

        if returnOp:
            return operations
        else:
            result = service.mutate(operations)

def removeCriteria(service, campaignId, locIds, targetList, returnOp=False):
    """
    Remove a location criteria from a campaign.
    Requires the ID of location criteria you wish to remove.
    """
    operations = []
    for id in locIds:
        if isinstance(id, str):
            pass
        else:
            if id['name'] not in targetList:
                pass
            else:
                operations.append(
                    {
                        'operator': 'REMOVE',
                        'operand': {
                            'campaignId': campaignId,
                            'criterion': {
                                # Need to know the id of the location that is
                                # targeted in order to remove it.
                                'id': id['id']
                            }
                        }
                    }
                )
    if operations:
        if returnOp:
            return operations
        else:
            result = service.mutate(operations)
    else:
        return("Nothing to remove.")

def updateCriteria(service, campaignId, dictToUpdate, targets, bidMod, returnOp=False):
    """
    Update a location criteria with the new bid modifier specified.
    In order to update a location criteria, you need to compare
    the old vs the new.
        If there are any changes, you remove the old and add the new.
        If there are no changes, nothing is done.

    This function only checks whether the parameter bidMod is different compared
    to the one present. It leaves the removing and adding to other functions.

    It is considered a best practice to group different mutate calls together.
    Instead of calling API to remove, and then call API again to add,
    group the remove and add operations together and then call API.
    """
    operations = []
    # bidMod = round(bidMod, 2)

    targets2 = getCriteriaWithBid(service, campaignId)

    notTargets = []
    i = 0
    while i < len(targets2):
        # Check wether bidMod changed.
        if bidMod == targets2[i]['bidMod']:
            notTargets.append(targets2[i]['name'])
            i += 1
        else:
            i += 1
    for loc in dictToUpdate:
        if isinstance(loc, str):
            pass
        else:
            # Checking for keys called 'id' and 'name'.
            if 'id' and 'name' in loc:
                # Check wether the location is being targeted.
                if loc['name'] in targets:
                    # Check if location has a new bidMod.
                    if loc['name'] not in notTargets:
                        # To update a criteria, first remove it.
                        op1 = removeCriteria(service, campaignId, [loc],
                            targets, returnOp=True)
                        # Then add it.
                        op2 = addCriteria(service, campaignId, [loc],
                            targets, bidMod, returnOp=True, doChecks=False)
                        if isinstance(op1, list) and isinstance(op2, list):
                            for item in op1:
                                operations.append(item)
                            for item in op2:
                                operations.append(item)
                        else:
                            print('can only add lists.')
                    else:
                        print('"%s": Update not needed.' % loc['name'])
                else:
                    print('"%s": You are trying to update a location that does '
                        'not yet exist.'
                        '\nUse "addCriteria" instead.\n' % loc['name'])
            else:
                print('"dictToUpdate" needs keys called "id" and "name".')
    if operations:
        if returnOp:
            return operations
        else:
            service.mutate(operations)
    else:
        return('Operations list is empty. Can not update anything.')

def callCampaignCritApi(service, operationsList):
    service.mutate(operationsList)
