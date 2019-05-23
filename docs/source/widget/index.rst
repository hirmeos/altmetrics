Metrics Widget
==============

The metrics-widget is currently under development, and currently, a prototype is
available. This document will describe how to include it in a web page.


Include CSS in your page
------------------------

The widget has been built using Bootstrap 4, as well as some custom CSS.

    .. code-block:: html

        <!-- load css for this app-->
        <link rel="stylesheet" href="https://storage.googleapis.com/hirmeos/metrics-widget/hirmeos-metrics-prototype-0.0.2.css">

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
              "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImcwN2gzMjEyQGdtYWlsLmNvbSJ9.ZUjknVXs52LGoudGH4YYFO6yAs7ukIMtJxclplfGIZ8",
              "uri": "info:doi:10.5334/bbc",
              "widgetTitle": "Metrics",
            };
        </script>

        <!-- load js for the Metrics Widget app-->
        <script src="https://storage.googleapis.com/hirmeos/metrics-widget/hirmeos-metrics-prototype-0.0.2.min.js"></script>


Widget customisation
--------------------

The widget can be customised by setting values in the widget_params variable.
Currently these include:

    - ``token``: The JWT used to authenticate yourself on the metrics-api
      (same token use for the altmetrics service).

    - ``uri``: The URI of the book / Chapter you want to display metrics for.

    - ``WidgetTitle``: The title that appears on the widget (defaults to 'Metrics').

Both ``token`` and ``uri`` need to be set in order for the widget to work.
