Annotation
==========

The aim of this section is to guide the partner through the integration of their
publishing platform with Hypothes.is and the CrossRef Event Data API, which is
the first step in order to get their data (and annotation) ingested into the
HIRMEOS Metrics service(s).

The Hypothes.is integration
---------------------------

A couple of quick remarks from the backend perspective:

* annotations are saved and stored in the Hypothes.is services
* annotations are associated with the URL of the page

CDN
...

Ubiquity Press has set up a CDN serving all the required libraries, except the
Hypothes.is library. A quick overview of the reasons to have libraries served by
a CDN:

* all the required libraries are available from the same resource
* all the required libraries are tied to a specific version of the bundle (see
  more below) and can be upgraded altogether, changing the version in the URL
* the CDN manager (Ubiquity Press) will take care of creating new bundles when
  the libraries are upgraded, and this will happen consistently with the
  developments in the libraries and the related platforms (Hypothes.is)

The CDN folders are structure as follows:

.. code-block:: html

    https://storage.googleapis.com/operas/<version>/<name>

Where:

``version``
  version of the JS bundle, (e.g. ``v1``, ``v2``)

``name``
  name of the library


The following table contains a list of the available libraries:

+---------------+---------------------------------------------------------+
| library       | public link                                             |
+===============+=========================================================+
| epub.js       | https://storage.googleapis.com/operas/v1/epub.js        |
+---------------+---------------------------------------------------------+
| epub.min.js   | https://storage.googleapis.com/operas/v1/epub.min.js    |
+---------------+---------------------------------------------------------+
| pdf.js        | https://storage.googleapis.com/operas/v1/pdf.js         |
+---------------+---------------------------------------------------------+
| pdf.worker.js | https://storage.googleapis.com/operas/v1/pdf.worker.js  |
+---------------+---------------------------------------------------------+

HTML
....

The best and up to date resource to learn how to set up Hypothes.is annotations
on an HTML page is the Hypothes.is `Quickstart`_ guide.

.. _Quickstart: https://web.hypothes.is/help/embedding-hypothesis-in-websites-and-platforms/

EPUB
....

At the most basic level, the only resources required to enable annotations on an
EPUB are the Hypothes.is CDN, ``jszip 3.1.5`` and ``epub.js 0.3.66``:

.. code-block:: html

    <script src="https://cdn.hypothes.is/hypothesis"></script>
    <script src="https://storage.googleapis.com/operas/v1/jszip.min.js"></script>
    <script src="https://storage.googleapis.com/operas/v1/epub.min.js"></script>

`This link`_ hosted by Hypothes.is contains a working implementation.
In the example, a function in ``reader.js`` is called when loading the page.
This function initialises an epub.js reader and enables Hypothes.is annotation
throughout the page, including within the EPUB content.
The code for this working implementation can be found in `this git repository`_.

.. _`This link`: https://cdn.hypothes.is/demos/epub/epub.js/index.html?loc=titlepage.xhtml
.. _`this git repository`: https://github.com/futurepress/hypothesis-reader

PDF
...

TBC

Embed Dublin Core
-----------------

It is clear that in order to make easier to calculate metrics around published
content, we need to associate the annotations with a unique identifier for the
published content, most often the DOI.

The CrossRef Event Data service scans known websites in order to retrieve URLs
for the content and associate them with DOIs. To make this happen, the content
page should contain Dublin Core Meta tags.

.. _plugin: https://web.hypothes.is/start/

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

.. code-block:: text

    https://metrics-api.operas-eu.org/events?filter=work_uri:info:doi:10.5334/bbc,measure_uri:https://metrics.operas-eu.org/hypothesis/annotations/v1

