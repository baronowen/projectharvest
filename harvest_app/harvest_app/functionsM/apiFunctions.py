from googleads import adwords

from harvest_app.api_calls import accounts, campaigns
from harvest_app.api_calls import campaignCriterion, locationCriterion

def createClient():
    """
    Loads in the credentials from the googleads.yaml file.
    """
    client = adwords.AdWordsClient.LoadFromStorage(path='data/config file API/googleads.yaml')
    return client

def createService(client, type, version='v201809'):
    if type == 'account':
        service = client.GetService('ManagedCustomerService', version=version)
        return service
    elif type == 'campaign':
        service = client.GetService('CampaignService', version=version)
        return service
    elif type == 'locationCriterion':
        service = client.GetService('LocationCriterionService', version=version)
        return service
    elif type == 'campaignCriterion':
        service = client.GetService('CampaignCriterionService', version=version)
        return service
    else:
        pass
# ------------------------------------------------------------------------------
def loadAccounts():
    client = createClient()
    service = createService(client, 'account')
    # Get all accounts.
    accountList = accounts.getAllAccounts(service)
    return accountList
# ------------------------------------------------------------------------------
def loadCampaigns():
    client = createClient()
    service = createService(client, 'campaign')
    # Get all campaigns.
    campaignList = campaigns.getAllCampaigns(service)
    return campaignList

def load1Campaign(id):
    client = createClient()
    service = createService(client, 'campaign')
    # Get 1 campaign by ID.
    campaign = campaigns.getCampaignById(service, id)
    return campaign
# ------------------------------------------------------------------------------
def loadCampaignCriteriaWithBid(campaignId):
    client = createClient()
    service = createService(client, 'campaignCriterion')
    # Get campaign location criteria in a dictionary.
    cDict = campaignCriterion.getCriteriaWithBid(service, campaignId)
    return cDict
# ------------------------------------------------------------------------------
def addCampaignCriteria(campaignId, postcode, targetList, bidModifier=0, returnOp=False):
    client = createClient()
    serviceL = createService(client, 'locationCriterion')
    serviceC = createService(client, 'campaignCriterion')
    # Look up location IDs.
    newLocs = locationCriterion.lookUpLocationsByName(serviceL, postcode)
    # Add location criteria to a campaign ID.
    temp = campaignCriterion.addCriteria(serviceC, campaignId, newLocs,
        targetList, bidModifier, returnOp=returnOp)
    return temp

def removeCampaignCriteria(campaignId, postcodes, targetList):
    client = createClient()
    serviceL = createService(client, 'locationCriterion')
    serviceC = createService(client, 'campaignCriterion')
    # Look up location IDs.
    locIds = locationCriterion.lookUpLocationsByName(serviceL, postcodes)
    # Remove location criteria on a campaign ID, using the location IDs.
    temp = campaignCriterion.removeCriteria(serviceC, campaignId, locIds, targetList)
    return temp

def updateCampaignCriteria(campaignId, postcodes, targetList, bidMod, returnOp=False):
    client = createClient()
    serviceL = createService(client, 'locationCriterion')
    serviceC = createService(client, 'campaignCriterion')
    # Look up location IDs.
    locIds = locationCriterion.lookUpLocationsByName(serviceL, postcodes)
    # Update bid modifier of a campaign criteria.
    temp = campaignCriterion.updateCriteria(serviceC, campaignId, locIds,
        targetList, bidMod, returnOp=returnOp)
    return temp

def callCampCritApi(operationsList):
    client = createClient()
    service = createService(client, 'campaignCriterion')
    temp = campaignCriterion.callCampaignCritApi(service, operationsList)
    return temp
