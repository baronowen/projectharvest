from googleads import adwords
# import api_calls.accounts
import api_calls.ac_delegators
# import api_calls.criterionDelegators

"""
This file was used to test the API functions before implementing them in the GUI.
"""

client = adwords.AdWordsClient.LoadFromStorage()
version = 'v201809'
# campaignId='1631705263'
# ------------------------------------------------------------------------------
# list = api_calls.criterionDelegators.delegateCall_cc(client, 'getCriteria',
#     version, campaignId='1631705263')
# print('getCriteria: ', list)
# # print(criterion)
#
# results2 = api_calls.criterionDelegators.delegateCall_cc(client, 'getCriteriaWithBid',
#     version, campaignId='1631705263')
# print('get2: ', results2)
#
# print('\nlocationCriteria')
# locations = api_calls.criterionDelegators.delegateCall_lc(client, 'lookUp', version,
#     locationNames=['AL6'])
# print('lookup: ', locations, '\n')
#
# api_calls.criterionDelegators.delegateCall_cc(client, 'updateCriteria', version,
#     campaignId='1631705263', dictToUpdate=locations, targets=list,
#     bidMod=1.15)

# api_calls.criterionDelegators.delegateCall_cc(client, 'addCriteria', version,
#     campaignId=campaignId, locIds=locations, targetList=list, bidModifier=0)
#
# api_calls.criterionDelegators.delegateCall_cc(client, 'removeCriteria', version,
    # campaignId='1631705263', locIds=locations, targetList=list)

# ------------------------------------------------------------------------------
"""Account creation"""
# print('account creation')
# api_calls.ac_delegators.delegateCall_a(client, 'add1', version)

"""Get accounts"""
# print('All accounts')
# accounts = api_calls.ac_delegators.delegateCall_a(client, 'getAll', version)
# print(accounts)
# for account in accounts:
#     print(account)

""""Campaign creation (includes budget)"""
# budgetId = api_calls.abc_delegators.delegateCall_b(client, 'add1', version)
# api_calls.abc_delegators.delegateCall_c(client, 'add1', version,
    # budgetId='1682210374')

""""Get campaigns"""
print('All campaigns:')
campaigns = api_calls.ac_delegators.delegateCall_c(client, 'getAll', version)
if isinstance(campaigns, str):
    print(campaigns)
else:
    for campaign in campaigns:
        print(campaign)
#
# print('One Campaign:')
# campaign = api_calls.abc_delegators.delegateCall_c(client, 'get1', version,
#     campaignId='1631705263')
# if isinstance(campaign, str):
#     print(campaign, '\n')
# else:
#     print(campaign)

"""Update status of campaigns"""
# campaign = api_calls.abc_delegators.delegateCall_c(client, 'updateStatus', version,
#     campaignIds=['1632395427'], status='PAUSED')
# if isinstance(campaign, str):
#     print(campaign)
# else:
#     print(campaign)

"""Update budgetId of campaigns"""
# campaign = api_calls.abc_delegators.delegateCall_c(client, 'updateBudget', version,
#     campaignIds=['1631705263'], budgetId='1682210374')
# print(campaign)
