Metrics Widget
==============

The metrics-widget has been released. This document will describe how to
include it in a web page.


Hosting of the Widget Code
--------------------------

The Widget code consists of two files that are hosted on the Ubiquity Press CDN,
https://storage.googleapis.com/hirmeos/metrics-widget/. These files are
``hirmeos-metrics.css`` and ``hirmeos-metrics.min.js``.

Versioning and Updates to the the Widget code
---------------------------------------------

Because JavaScript code gets cached by Browsers, updates to the Widget code
require these files to be renamed so they are downloaded.As a result, the Widget
files are named based on their release versions.

Descried in this document, these are ``hirmeos-metrics-0.1.1.min.js`` and
``hirmeos-metrics-0.1.1.css``. The CSS and JavaScript files are released and
versioned together to ensure that CSS files with a given version will support
HTML that is created in JavaScript files with the same version.

Please remember to update **both** the CSS and JavaScript files when using a
newer version of the Widget.

Include CSS in your page
------------------------

The widget has been built using Bootstrap 4, as well as some custom CSS.

    .. code-block:: html

        <!-- load css for this app-->
        <link rel="stylesheet" href="https://storage.googleapis.com/hirmeos/metrics-widget/hirmeos-metrics-0.1.1.css">

        <!--load bootstrap-->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">


Decide where you want the widget to appear
------------------------------------------

To place the widget in your page, add the following <div> element, keeping the
id as is.

    .. code-block:: html

        <div id="metrics-block"></div>


Include widget JavaScript
-------------------------

The widget has been built React, so this will need to be imported, along with
the JavaScript of the widget itself. Make sure these scripts are included in the
order shown.

You will need to edit the values in ``widget_params``.

    .. code-block:: html

        <!-- React -->
        <script src="https://unpkg.com/react@16.4.1/umd/react.production.min.js"></script>
        <script src="https://unpkg.com/react-dom@16.4.1/umd/react-dom.production.min.js"></script>

        <!-- Customise Widget parameters -->
        <script>
            let widget_params = {
              "uri": "info:doi:10.5334/bbc",
            };
        </script>

        <!-- load js for the Metrics Widget app-->
        <script src="https://storage.googleapis.com/hirmeos/metrics-widget/hirmeos-metrics-0.1.1.min.js"></script>


Widget customisation
--------------------

The widget can be customised by setting values in the widget_params variable.
Currently these include:

    - ``uri``: Required - The URI of the book / Chapter you want to display
      metrics for.

    - ``locale``: Language code for locale that the widget should be displayed
      in (default is 'en').

    - ``baseUrl``: Base URL for querying metrics. Can be set if you have a local
      instance of the metrics API (defaults to "https://metrics.ubiquity.press").

    - ``WidgetTitle``: The title that appears on the widget
      (default is 'Metrics').

    - ``showDetailedMetricsLink``: ``true`` or ``false``, whether or not to
      display link to detailed metrics (if available; defaults to ``false``).

    - ``detailedMetricsLink``: URL link to detailed metrics (no default).

    - ``detailedMetricsText``: Text to show for displaying the link to detailed
      metrics (default is 'Show detailed metrics').


Only ``uri`` needs to be set in order for the widget to work.
