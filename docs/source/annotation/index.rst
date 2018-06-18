Annotation
==========

The aim of this section is to guide the partner through the integration of his
publishing platform with the CrossRef Event Data API, which is the first step in
order to get his data (and annotation) ingested into the HIRMEOS services.

The Hypothes.is plugin
----------------------

From the user's perspective, annotations can be created on any page using the
Hypothes.is browser plugin_. Once installed and opened, the user will be able to
create annotation on the selected content on the page.

A couple of quick remarks from the backend perspective:

* annotations are saved and stored in the Hypothes.is services
* annotations are associated with the URL of the page

It is clear that in order to make easier to calculate metrics around published
content, we need to associate the annotations with a unique identifier for the
published content, most often the DOI.

The CrossRef Event Data service scans known websites in order to retrieve URLs
for the content and associate them with DOIs. To make this happen, the content
page should contain Dublin Core Meta tags.

.. _plugin: https://web.hypothes.is/start/

Embed Dublin Core
-----------------

Something similar to the following code snippet should be used in order to allow
the CrossRef Event Data service to associate a published content page with a
DOI:

.. code-block:: html

    <head>
    <meta name="dc.identifier" content="10.1371/journal.pone.0160617"/>
    </head>

The Event Data documentation has a dedicated_ section on the best practices for
publishers.

.. _dedicated: https://www.eventdata.crossref.org/guide/best-practice/publishers-best-practice/

Check the HIRMEOS Metrics API
-----------------------------

What happens next:

* CrossRef Event Data will crawl the pages for annotations
* the HIRMEOS Metrics service will gather information on the Event Data API

The results are available on the HIRMEOS metrics, by source:

.. code-blocK:: guess

    https://metrics.ubiquity.press/api/altmetrics?uri=10.5334/dsj-2016-006&view=source&source=hypothesis

