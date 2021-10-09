
# "Panthera, Leo"

Lion's Own Taxonomic System

2021-10-03

Status: In Design


## Purpose

I keep a lot of notes, and use two types of tags to keep those notes organized:

1. **mnemonic tags** -- these are just *words,* that come to my mind, with no real formal signification system -- it's just about being able to locate a note by mnemonic association
2. **formal tags** -- these are tags that have a specific and curated meaning

This project is about being able to locate *formal tags* quickly.


## The Model

The following information is associated with a Formal tag:

* **tag** -- the string identifier of the tag (ex: `kowloonwalledcity`)
* **mnemonics** -- words that come to mind when you think of the tag -- (ex: `kowloon walled city archology china chinese city ruin`)
* **title** -- a title for the tag (ex: `Kowloon Walled City 九龍寨城`)
* **description* -- a text string, intended to store a few sentences describing the map
* **identifier** -- the identifier for the tag (ex: `tag:lionkimbro@gmail.com,2021-02-18:tag:kowloonwalledcity`)
  * note that the user can specify the identifier to be used, though one will be automatically generated from the user's chosen authority (an e-mail address or domain name that the user controls, as self-reported) and the present date (or a user selected fixed date)
* **creator** -- identifier of the creator of this tag (ex: `tag:lionkimbro@gmail.com,2021:person:lion`), as self reported
* **date created** -- the date the formal tag was first created (ex: `2021-02-18`)

Further more, the formal tags can appear on "maps," which are contexts wherein the tag is related with respect to other tags.

The following information is associated with a Map:

* **name** -- a string identifier, naming the map (ex: `citiesofchina`)
* **title** -- a human readable title for the map (ex: `Cities of China`)
* **map** -- a text string, intended for a monotype font, in which formal tags are named spatially, to illustrate a map of names
* **description** -- a text string, intended to store a few sentences describing the map
* **identifier** -- the identifier for the map (ex: `tag:lionkimbro@gmail.com,2021-02-18:map:cities-of-china`)
* **creator** -- identifier of the creator of this map (ex: `tag:lionkimbro@gmail.com,2021:person:lion`), as self reported
* **date created** -- the date the map was first created (ex: `2021-02-18`)

### Links

When a map mentions a tag, it is noted via a "map-mentions" link.

When a tag has a "see also" to another tag, it is noted via a "see-also" link.


## How Data Is Stored

Data is stored in "Entity Packages."  I'm actively (2021-10-03) developing this system, through [my Internet Office.](https://communitywiki.org/wiki/LionsInternetOffice).

In accordance with the Entity packages system, identifiers are either v4 UUIDs (when human readability is not necessary,) or [RFC4151 tag URIs](https://en.wikipedia.org/wiki/Tag_URI_scheme) (when human readability is desirable.)  Both forms of identifier are globally unique.


## Interface

I'm imagining:
* tcl/tk + Python (tkinter)
* Each tag is treated in its own window
* Each map is treated in its own window
* There is also a "settings" window, accessible from a menu.

Menu:  File (Add, Forget, Save, Save To, Exit), New (New Tag, New Map), Search (for Tag, for Map), Help (Tutorial, Contact, About)

Settings window: user's own tag, user's authority (e-mail addr or domain), prefix for default new tag identifiers ("%AUTH" for user's authority, "%YEAR" "%MONTH" or "%DAY%" for the current day's date,) help button next to each for hover-over explanations about each, 

Tag window: tag, tags for tag, mnemonics, title, description (larger text area), identifier + generating checkbox (does it mirror tag w/ shaping from settings), creator, date created, maps participated in, see also tags

Map window: name, title, map, description, identifier + generating checkbox (does it mirror name w/ shaping from settings), creator, data created


## Schema Involved

* Formal Tags -- `tag:lionkimbro@gmail.com,2021-10:schema:tag`
* Maps of Tags -- `tag:lionkimbro@gmail.com,2021-10:schema:map`
* Link: See Also -- `tag:lionkimbro@gmail.com,2021-10:schema:link:see-also`
* Link: Mentions -- `tag:lionkimbro@gmail.com,2021-10:schema:link:map-mentions`

