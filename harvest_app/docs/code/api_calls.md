# Package api_functions
All functions in this package create a client that retrieves the information from the `googleads.yaml` file.
After a client is created every function creates a service for the required operation. The functions that add and remove location criteria create two services, one for location criterion and one for campaign criterion.

The functions within the modules in this package act as a bridge or link between the GUI in `harvest_app/harvest_app/pages/` and the API functions in `harvest_app/harvest_app/api_calls/`.

## Accounts

This module is used to retrieve AdWords accounts through the AdWords API. The function that does this is <i>getAllAccounts</i>.

DISCLAIMER:
In order to retrieve accounts successfully, the ID of a manager (MCC) account needs to be present on startup in the `googleads.yaml` file. This file has to be located in `data/config file API/`.


<b>GetAllAccounts</b>
This function retrieves all account ID's and names through the API. It does this by creating a selector and sending a get request to the service (which is created in the delegator) with the created selector.

Parameters: None.

## Campaigns

This module is used to retrieve information about one or more AdWords campaigns through the API.
The functions that do this are:
* getAllCampaigns
Retrieve all campaigns under a client account. (Client ID has to be specified in the `googleads.yaml` file)
* getCampaignById
Retrieve one campaign with the specified campaign ID under the specified client account.

<b><u>GetAllCampaigns</u></b>
This function is used to retrieve all campaigns under a client account. This is done by building a query with the AdWords Query Language (AWQL). This query is then send to a `Pager` that returns the results.

Parameters: None.

<b><u>GetCampaignById</u></b>
This function is used to retrieve information about one specific campaign. This is also done with AWQL, by creating a query, specifying that the ID has to be equal to a specific ID and sending it to a  `Pager` that returns the result.

Parameters:
* campaignId
String type, used to retrieve that specific campaign.

## CampaignCriterion

This module is used to retrieve, add and remove (and update) location targeting campaign criteria. In Google AdWords, criterias store information regarding targeting and bidding options. One of these options is location targeting. Functions within this module can retrieve targeted locations, add new locations and remove locations.

Updating (overwriting) location targeting of a campaign is done by comparing the old list of targets with the new one, removing those that are not needed, and adding those that are needed. It used to be possible to overwrite location targeting using the `SET` operator, however, this behaviour is no longer supported.

For more information regarding location targeting in python, see the [Python Targeting Samples page][1] in the Google AdWords API documentation.

For more information on criteria usage, see the [Criteria usage page][2] of the Google AdWords API documentation.

<b><u>GetCriteriaWithBid</u></b>
This function returns a dictionary with the location name and the bid modifier for that location. This is done by creating a selector. This selector filters the result by using predicates that only select locatoin criteria with a specific campaign ID as well as a specific criteria type.
This selector is send to the service (created in the delegator) with a get request, which returns the information in an object like shape. A loop is started over this information which filters away the locations that are not a postcode and then adds the location name and bid modifier to a dictionary which is returned.

Parameters:
* campaignId
String type, used to only retrieve location criteria for that campaign.

<b><u>AddCriteria</u></b>
This function is used to add a location criteria to a campaign. In order to add a new location, the ID of that location is needed. This is done by calling `lookUpLocationsByName`. A detailed explanation of this function will be in its own section.
The adding is done by first creating a criterion. This criterion contains the `xsi_type` and the `id`. The `xsi_type` is `'Location'` and the `id` is the ID of that specific location. These criterions are then added to a list.
If there are entries in this list, a loop is started that adds operations to another list. Each operation has an `operator` (`'ADD'`) and its `operand`. The `operand` has a `campaignId` and a `criterion`. The `operand` can potentially also have a `bidModifier`.
When this operations list is done, a mutate request is send to the service, with the operations list.

It is considered a best practice to group mutate calls together in one API call.

Mandatory parameters:
* campaignId
String type, needed to add a criteria.
* locIds
List of dictionaries, containing the name and ID of a location, e.g.
  ```python
  [{'id': 9046018, 'name': 'AL6'}]
  ```
* targetList
List type, contains the names of all locations currently being targeted, under this   campaign.
* bidModifier
Integer type, represents the bid modifier.

Optional parameters:
* returnOp
Boolean type, used to determine whether the operations list is returned to caller, or send to API.
* doChecks
Boolean type, used to determine whether checks need to be done or not.

<b><u>RemoveCriteria</u></b>
This function is used to remove a criteria from a campaign. Just like with adding, the ID of the location that is to be removed is necessary. This is done by calling `lookUpLocationsByName`.

Before removing, a check is run over all locations that are to be removed. This 'check' checks wether the locations are currently being targeted, since you can't remove one if it isn't targeted.
Once this is done, operations are added to a operations list. Each operation has an `operator` (`'REMOVE'`) and its `operand`. The `operand` has a `campaignId` and a `criterion`, this `criterion` in turn has a field `id`, which contains the ID of the location that is to be removed.
When the operations list is done, a mutate request is send to the service, with the operations list.

Mandatory parameters:
* campaignId
String type, needed to remove a location criteria.
* locIds
List of dictionaries, containing the name and ID of a locations, e.g.
  ```python
  [{'id': 9046018, 'name': 'AL6'}]
  ```
* targetList
List type, contains the names of all locations currently being targeted, under this campaign.

Optional parameters:
* returnOp
Boolean type, used to determine whether the operations list is returned to caller, or send to API.

<b><u>UpdateCriteria</u></b>
This function doesn't actually update a location criteria, since it is not possible to overwrite existing criteria. Instead, this functions first checks whether the bid modifier changes for a location criteria. If the bid modifier doesn't change, it is added to a list called `notTargets`.
When this is done, the function checks for each location whether it is currently being targeted. If it is being targeted, it checks whether it is in `notTargets`. If a location is not, it first calls the function `removeCriteria` and then `addCriteria`, both with `returnOp` on `True`, and adds the operations that came out of this to a list.
When the loop is done, the list is send with a mutate request to the service.

Parameters:
* campaignId
String type, needed to 'update' a campaign criteria.
* dictToUpdate
List of dictionaries, containing the name and ID of the locations that are to be 'updated'.
  ```python
  [{'id': 9046018, 'name': 'AL6'}]
  ```
* targets
List type, containing the names of all locations currently being targeted, under this campaign.
* bidMod
Integer type, represents the bid modifier.

<b><u>CallCampaignCritApi</u></b>
A very small function, which only purpose is to send a mutate request with operations to the AdWords API. This function is used when auto targeting the best categories and was made to conform to the best practice of grouping mutate requests together.

## LocationCriterion

This module has only one purpose, which is the retrieval of the ID of one or more locations that are to be retrieved, added or removed. The function that does this is `lookUpLocationsByName`.

For more information regarding the retrieval of location criteria by name, see the [Targeting Samples page][3] in the Google AdWords API documentation.

<b><u>LookUpLocationsByName</u></b>
This function creates a list of dictionaries with the name and ID of a location. This is done by creating a selector. This selector has a predicate that only selects the locations with the specified location name. The selector is then send to the service with a get request.
When something is returned, a loop is started that checks whether the `displayType` of a criterion is `'Postal Code'`. If this is true it checks whether the location name is in the list called `locationNames`. If this is also true it creates a dictionary which is returned.

Parameters:
* locationNames
List of strings, containing the names of locations, e.g.
  ```python
  ['AL1', 'AL10', 'CR0']
  ```


[1]: https://developers.google.com/adwords/api/docs/samples/python/targeting#add-targeting-criteria-to-a-campaign
[2]: https://developers.google.com/adwords/api/docs/appendix/criteria-usage
[3]: https://developers.google.com/adwords/api/docs/samples/python/targeting#get-location-criteria-by-name
