from googleads import adwords
import datetime
pageSize = 100

def getAllCampaigns(service):
    """
    Retrieve all campaigns under a account.

    No campaigns will be returned when this function is ran from
    an MCC account (having a MCC ID in googleads.yaml).
    """
    # Using AWQL to retrieve campaigns.
    query = (adwords.ServiceQueryBuilder()
        .Select('Id', 'Name', 'Status', 'StartDate', 'EndDate',
            'BudgetId', 'BudgetStatus', 'BudgetName', 'Amount',
            'BudgetReferenceCount', 'IsBudgetExplicitlyShared')
        .Limit(0, pageSize)
        .Build())
    campaigns = []
    for page in query.Pager(service):
        if page['entries']:
            for campaign in page['entries']:
                campaigns.append(campaign)
        else:
            pass
    return campaigns

def getCampaignById(service, campaignId):
    """
    Retrieve the campaign with the specified campaign ID.
    """
    endCampaign = None
    # Again using AWQL to retrieve campaigns.
    query = (adwords.ServiceQueryBuilder()
        .Select('Id', 'Name', 'CampaignGroupId', 'Status', 'ServingStatus',
            'StartDate', 'EndDate',
            'BudgetId', 'BudgetName', 'BudgetStatus', 'Amount',
            'DeliveryMethod', 'BudgetReferenceCount', 'IsBudgetExplicitlyShared',
            'Settings')
        .Where('Id').EqualTo(campaignId)
        .Limit(0, 1)
        .Build())
    for page in query.Pager(service):
        if page['entries']:
            for campaign in page['entries']:
                endCampaign = campaign
        else:
            pass
    return endCampaign
